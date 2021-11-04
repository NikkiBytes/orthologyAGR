
import os
import numpy as np
import pandas as pd
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
    infile = os.path.join(data_folder, "ORTHOLOGY-ALLIANCE_COMBINED_51.tsv")
    assert os.path.exists(infile)

    # use pandas to load -- update to use built-in package from utils !!!!!
    data_ortho=pd.read_csv(infile, header=15, sep="\\t", engine='python').sort_values(by=['Gene1ID']) 
    #data_ortho=data_ortho.to_dict(orient='records')
    #data_ortho=data_ortho.sort_values(by=['Gene1ID']) 
    #display(data_ortho[:5])
    
    # get unique value of ids from Gene1ID column
    unique_ids=data_ortho["Gene1ID"].unique()

    final_list=[] # initialize final data list
    bad_queries=[] # initialize gene query ids that return None (empty)
    

    process_key = lambda k: k.replace(" ","_").lower() 

    # initialize mygene object
    gene_client = get_client('gene')

    for gene_id in unique_ids[:4]:
        pairwise_check, gene_df=orthology_search(gene_id, data_ortho)
        if pairwise_check==True:
            
            if ":" in gene_id: gene_id=gene_id.split(":")[1]
            # query for the corresponding numeric id of the original id
            gene=get_gene(gene_id, gene_client)
            
            # check if gene id was not found
            if not gene:
                bad_queries.append(gene_id) # add no matching id
            else:
                gene_id = gene["_id"] # assign new id queried from mygene

            # convert df into records
            gene_df=gene_df.to_dict(orient='records')

            record_list=[]
            for rec in gene_df[:3]:
                gene2_id=rec["Gene2ID"]
                if ":" in gene2_id: gene2_id=gene2_id.split(":")[1]

                gene2=get_gene(gene2_id, gene_client)

                if not gene2:
                    bad_queries.append(gene2_id) # add no matching id
                else:
                    gene2_id = gene2["_id"] # assign new id queried from mygene

                # clean up data
                rec = dict_convert(rec,keyfn=process_key)
                # remove NaN values, not indexable
                rec = dict_sweep(rec,vals=[np.nan])

                # setup document
                doc=set_document(rec)
                doc["geneid"]=gene2_id
                # add to the results
                #results.setdefault(_id,[]).append(doc)

                record_list.append(doc)
            
            #print(json.dumps(record_list[:3], sort_keys=False, indent=4))
            id_record = {"_id": gene_id, "agr": {"orthologs": record_list}}

            final_list.append(id_record)
        
        else:
            continue
    
    # print(json.dumps(final_list[:5], sort_keys=False, indent=4))
    return final_list;