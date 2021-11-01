
import os, pandas
import numpy as np

from biothings_client import get_client
from biothings.utils.dataload import dict_convert, dict_sweep
from biothings import config

logging = config.logger

def setup_release(self):
    release="2019-06-23"
    return release

# boolean conversion method
def convert_score(score):
    if score=="Yes":
        return True;
    else:
        return False;

# document setup method
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
    return gene_client.getgene(gene_id, fields='symbol,name');
   

# main method 
def load_orthology(data_folder):
    # setup data from the file
    infile = os.path.join(data_folder, "ORTHOLOGY-ALLIANCE_COMBINED.tsv")
    assert os.path.exists(infile)

    # use pandas to load -- update to use built-in package from utils !!!!!
    data_ortho=pandas.read_csv(infile, header=15, sep="\\t", engine='python').to_dict(orient='records')

    final_list=[] # initialize final data list
    bad_queries=[] # initialize gene query ids that return None (empty)

    process_key = lambda k: k.replace(" ","_").lower() 

    # initialize mygene object
    gene_client = get_client('gene')

    # iterate over the data
    for rec in data_ortho[:50]:

        try:
            # get the main ID and reformat 
            orig_id1= rec["Gene1ID"].split(':')
            id1_tag2=orig_id1[1]
            _id = id1_tag2

            # query for the corresponding numeric id of the original id
            gene=get_gene(_id, gene_client)
            
            # check if gene id was not found
            if not gene:
                bad_queries.append(_id) # add no matching id
            else:
                _id = gene["_id"] # assign new id queried from mygene

            rec = dict_convert(rec,keyfn=process_key)
            # remove NaN values, not indexable
            rec = dict_sweep(rec,vals=[np.nan])

            # setup document
            doc=set_document(rec)
            
            # add to the results
            #results.setdefault(_id,[]).append(doc)

            final_doc = {"_id": _id, "agr": {"ortholog" : doc}}
            final_list.append(final_doc)

        except:
            continue

    #print(json.dumps(final_list[:3], sort_keys=False, indent=4))
    return final_list;
