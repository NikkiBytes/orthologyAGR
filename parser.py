"""
# Orthology AGR Data Parser  
# Author: Nichollette T. Acosta  
# Organization: Su and Wu labs @ Scripps Research  
# Data parser for the Alliance of Genome Resources database for orthology relationships. 
"""
# load packages
import os
import pandas as pd
import numpy as np

from biothings_client import get_client
from biothings.utils.dataload import dict_convert, dict_sweep
from biothings import config

logging = config.logger

def setup_release(self):
    release="2019-06-23"
    return release

def convert_score(score):
    if score=="Yes":
        return True;
    else:
        return False;


def set_document(rec):
    doc={
        "geneid": rec['gene2id'],
        "symbol": rec['gene2symbol'],
        "taxid": int(float(rec['gene2speciestaxonid'].split(":")[1])),
        "algorithmsmatch": rec["algorithmsmatch"],
        "outofalgorithms": rec["outofalgorithms"] ,
        "isbestscore": convert_score(rec['isbestscore']),
        "isbestrevscore": convert_score(rec['isbestrevscore'])
    }
    return doc;


# gene query method
def get_gene(gene_id, gene_client):
    # initialize mygene object
    gene=gene_client.getgene(gene_id, fields='symbol,name')
    return gene;

def orthology_search(gene_id, df):
    if df.loc[df["Gene1ID"].isin([gene_id])].shape[0] == df.loc[df["Gene2ID"].isin([gene_id])].shape[0]:
        return True, df.loc[df["Gene1ID"].isin([gene_id])];
    else:
        return False, df.loc[df["Gene1ID"].isin([gene_id])];


# Build Parser 
def load_orthology(data_folder):
    # setup data from the file
    infile = os.path.join(data_folder, "ORTHOLOGY-ALLIANCE_COMBINED.tsv")
    zfin_ncbi_file=os.path.join(data_folder, "gene.txt")

    assert os.path.exists(infile)

    # use pandas to load -- update to use built-in package from utils !!!!!
    data_ortho=pd.read_csv(infile, header=15, sep="\\t", engine='python')#.sort_values(by=['Gene1ID']) 
    zfin_df=pd.read_csv(zfin_ncbi_file, sep="\\t", header=1, engine='python')

    # get unique value of ids from Gene1ID column
    unique_ids=data_ortho["Gene1ID"].unique()

    final_list=[] # initialize final data list
    bad_queries=[] # initialize gene query ids that return None (empty)
    

    process_key = lambda k: k.replace(" ","_").lower() 

    # initialize mygene object
    gene_client = get_client('gene')

    for gene1_id in unique_ids[:10]:
        pairwise_check, gene_df=orthology_search(gene1_id, data_ortho) # get the orthology relationship
        if pairwise_check==True:
            
            if ":" in gene1_id : gene1_id = gene1_id.split(":")[1]
            
            # query for the corresponding numeric id of the original id
            gene=get_gene(gene1_id, gene_client)
            
            # check if gene id was not found
            if not gene:

                # check if gene in ZFIN database
                if "Z" in gene1_id:
                    try:
                        temp_df=zfin_df.loc[zfin_df["ZFIN ID"] == gene1_id ]
                        gene1_id=temp_df["NCBI Gene ID"].values[0]
                    except:
                        bad_queries.append(gene1_id)

                else:
                    bad_queries.append(gene1_id) # add no matching id
            else:
                gene1_id = gene["_id"] # assign new id queried from mygene

            # convert df into records
            gene_df=gene_df.to_dict(orient='records')

            record_list=[] # initialize gene1ID record list 
            for rec in gene_df:
                gene2_id=rec["Gene2ID"]
                if ":" in gene2_id: gene2_id=gene2_id.split(":")[1]

                gene2=get_gene(gene2_id, gene_client)

                if not gene2:
                    if "Z" in gene2_id:
                        try:
                            temp_df=zfin_df.loc[zfin_df["ZFIN ID"] == gene2_id ]
                            gene2_id=temp_df["NCBI Gene ID"].values[0]
                        except:
                            if gene2_id not in bad_queries: bad_queries.append(gene2_id) 
                            
                    else:
                        if gene2_id not in bad_queries: bad_queries.append(gene2_id) # add no matching id
                else:
                    gene2_id = gene2["_id"] # assign new id queried from mygene

                # clean up data
                rec = dict_convert(rec,keyfn=process_key)
                # remove NaN values, not indexable
                rec = dict_sweep(rec,vals=[np.nan])

                # setup document
                doc=set_document(rec)
                doc["geneid"]=gene2_id
            
                record_list.append(doc)
            
            id_record = {"_id": gene1_id, "agr": {"orthologs": record_list}}

            final_list.append(id_record)
        
        else:
            continue
    
    return final_list;
