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
#from biothings import config

#logging = config.logger

def setup_release(self):
    release="2019-06-23"
    return release

def convert_score(score):
    """
        Converts the isbestscore and isbestrevscore 
        from a string to boolean. 
        score: "Yes" or "No" string 
    """
    if score=="Yes":
        return True;
    else:
        return False;

def set_document(rec, gene2_id):
    """
        Fill in the ortholog record from gene2 ID
        rec: record dictionary
        gene2_id: ortholog entrezgene ID   
    """
    doc={
        "geneid": gene2_id,
        "symbol": rec['gene2symbol'],
        "taxid": int(float(rec['gene2speciestaxonid'].split(":")[1])),
        "algorithmsmatch": rec["algorithmsmatch"],
        "outofalgorithms": rec["outofalgorithms"] ,
        "isbestscore": convert_score(rec['isbestscore']),
        "isbestrevscore": convert_score(rec['isbestrevscore'])
    }
    return doc;

def get_entrezgene(gene_id, gene_client, bad_queries):
    """
        Use the biothings_client package to query the mygene.info db for 
        the corresponding entrezgene(NCBI gene) ID for the given gene_id
        gene_id: given id to search on
        gene_client: initialized object for connection to mygene.info 
    """
    #gene_client = get_client('gene') # initialize mygene object
    if "WB:" in gene_id: gene_id=gene_id.replace("WB:", "WormBase:")
    if "FB:" in gene_id: gene_id=gene_id.replace("FB:", "FLYBASE:")
    #gene=gene_client.getgene(gene_id, fields='symbol,name')

    #print("[INFO] searching for gene id ", gene_id)
    gene=gene_client.query(gene_id, fields='symbol,name') # get search results
    # check if gene id was not found
    if not gene["hits"]:
        #print("[INFO] Failed query on ID %s "%gene_id)
        bad_queries.append(gene_id)
    else:
        #print("[INFO] Success query on ID %s "%gene_id)
        gene_id=gene["hits"][0]["_id"]

    return gene_id, bad_queries;

def pairwise_check(gene_id, df, failed_pairwise):
    """
        Pairwise relation check for given gene_id
        gene_id: gene to search on
        df: input data 
        failed_pairwise: list for any failed ids  
    """
    # get the list of relationships for gene_id
    l1=list(df.loc[df["Gene1ID"].isin([gene_id])]["Gene2ID"])
    l2=list(df.loc[df["Gene2ID"].isin([gene_id])]["Gene1ID"])
    
    #compare the lists for a match
    if set(l1) != set(l2):
        pairwise_check_fails.append(gene_id)
        
    return df.loc[df["Gene1ID"].isin([gene_id])], failed_pairwise;

# Build Parser 
def load_orthology(data_folder):
    """
        Main Method - data plugin parser for ortholog data from AGR
        data_folder: input folder (standard for biothings studio plugin)
    """
    #print("[INFO] loading orthology AGR data....")
    
    # setup data from the file
    infile = os.path.join(data_folder, "ORTHOLOGY-ALLIANCE_COMBINED_51.tsv")
    assert os.path.exists(infile)

    # use pandas to load -- update to use built-in package from utils !!!!!
    data_ortho=pd.read_csv(infile, header=15, sep="\\t", engine='python')#.sort_values(by=['Gene1ID']) 

    # get unique value of ids from Gene1ID column
    unique_ids=data_ortho["Gene1ID"].unique()

    final_list=[] # initialize final data list
    bad_queries=[] # initialize gene query ids that return None (empty)
    failed_pairwise=[] # initialize list to hold any failed pairwise checks

    process_key = lambda k: k.replace(" ","_").lower() 
    
    # loop through ids and create records 
    for gene1_id in unique_ids[:5]:

        # initialize mygene object
        gene_client = get_client('gene')
        # check the current gene IDs pairwise relatiion
        gene_df, failed_pairwise=pairwise_check(gene1_id, data_ortho, failed_pairwise) 

        # convert the ID to the corrersponding NCBI ID ("entrezgene") 
        gene1_id, bad_queries=get_entrezgene(gene1_id, gene_client, bad_queries)

        # convert df into records
        gene_df=gene_df.to_dict(orient='records')
        #print(gene_df[0])

        record_list=[] # initialize record list for orthologs
        for rec in gene_df:
            gene2_id=rec["Gene2ID"] # get ortholog id
            gene2_id, bad_queries=get_entrezgene(gene2_id, gene_client, bad_queries)
            
            # clean up data
            rec = dict_convert(rec,keyfn=process_key)
            # remove NaN values, not indexable
            rec = dict_sweep(rec,vals=[np.nan])

            # setup document
            doc=set_document(rec, gene2_id)
        
            record_list.append(doc)
        
        #print(json.dumps(record_list[:3], sort_keys=False, indent=4))
        id_record = {"_id": gene1_id, "agr": {"orthologs": record_list}}

        final_list.append(id_record) # append to the final data list

    #print("[INFO] completed loading data.")
    #print(json.dumps(final_list[:5], sort_keys=False, indent=4))

    return final_list;
