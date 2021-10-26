
import os, pandas
import numpy as np
from biothings.utils.dataload import dict_convert, dict_sweep
from biothings import config
logging = config.logger

process_key = lambda k: k.replace(" ","_").lower()

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
        "taxid": rec['gene2speciestaxonid'], 
        "algorithmsmatch": rec["algorithmsmatch"],
        "outofalgorithms": rec["outofalgorithms"] ,
        "isbestscore": convert_score(rec['isbestscore']),
        "isbestrevscore": convert_score(rec['isbestrevscore'])
    }
    return doc;

# gene query method
def get_gene(gene_id):
    gene=gene_client.getgene(gene_id, fields='symbol,name')
    return gene;


# main method 
def load_orthology(data, data_list):
    # gather data file 
    infile = os.path.join(data_folder, "ORTHOLOGY-ALLIANCE_COMBINED.tsv")
    assert os.path.exists(infile)
    data_ortho=pandas.read_csv(infile, header=15, sep="\\t").to_dict(orient='records')
    results = {} # initialize final result dict 
    bad_queries=[] # initialize gene query ids that return None (empty)
    process_key = lambda k: k.replace(" ","_").lower()

    # iterate over the data
    for rec in data_ortho:

        # get the main ID and reformat 
        orig_id1= rec["Gene1ID"].split(':')
        id1_tag2=orig_id1[1]
        _id = id1_tag2

        # query for the corresponding numeric id of the original id
        gene=get_gene(_id)
        
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
        results.setdefault(_id,[]).append(doc)

    # iterate through result items
    for _id,docs in results.items():
        doc = {"_id": _id, "agr": {"ortholog" : docs}}
        #print(json.dumps(doc, sort_keys=False, indent=4))
        yield doc
