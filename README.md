# Orthology AGR Data Plugin for BioThings   
  
## <u> Document Structure </u>
      
```
"_id": "WBGene00011502" --> "176377" by querying mygene.info API,
  "agr": 
     "ortholog": [
        {
          "geneid": "SGD:S000003566",
          "symbol": "VPS53",
          "taxid": "NCBITaxon:559292" --> 559292,
          "algorithmsmatch": 9,
          "outofalgorithms": 10,
          "isbestscore": "Yes" --> True,
          "isbestrevscore": "Yes" --> True
        }
```  



<br>  
<br>  

## Notes    
- The variable, `"algorithms": "PhylomeDB|OrthoFinder|Hieranoid|OMA|Ensembl Compara|Roundup|InParanoid|PANTHER|OrthoInspector"` is available in the data file. Currently the created output document doesn't include it, but can easily be added. Note, if added, we considered reformatting the data string into a list.

<br>

