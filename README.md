# Orthology Data Plugin  
**Data from Alliance of Genome Resources ([AGR](https://www.alliancegenome.org/downloads#orthology))** 
<br>  

## Notes    

- **Entity-Centric** document structure.  


- Translated the gene IDs given into the `entrezgene` id using `biothings_client`.   
- Confirmed the **pairwise relations** among IDs.  
- The variable, `"algorithms": "PhylomeDB|OrthoFinder|Hieranoid|OMA|Ensembl Compara|Roundup|InParanoid|PANTHER|OrthoInspector"` is available in the data file. The current output does not include it, however the variable can easily be added. Note, if added, we consider reformatting the data string into a list of strings. 

<br>
<br>

## <u> Document Structure </u>
      
```

[
    {
        "_id": "176377",
        "agr": {
            "orthologs": [
                {
                    "geneid": "S000003566",
                    "symbol": "VPS53",
                    "taxid": 559292,
                    "algorithmsmatch": 9,
                    "outofalgorithms": 10,
                    "isbestscore": true,
                    "isbestrevscore": true
                },
                {
                    "geneid": "33640",
                    "symbol": "Vps53",
                    "taxid": 7227,
                    "algorithmsmatch": 9,
                    "outofalgorithms": 10,
                    "isbestscore": true,
                    "isbestrevscore": true
                },   
                .  
                .  
                .  
                .    
                ]  
        }
    },
    {
        "_id": "492817",
        "agr": {
            "orthologs": [
                {
                    "geneid": "S000003566",
                    "symbol": "VPS53",
                    "taxid": 559292,
                    "algorithmsmatch": 8,
                    "outofalgorithms": 10,
                    "isbestscore": true,
                    "isbestrevscore": true
                },
                {
                    "geneid": "33640",
                    "symbol": "Vps53",
                    "taxid": 7227,
                    "algorithmsmatch": 9,
                    "outofalgorithms": 11,
                    "isbestscore": true,
                    "isbestrevscore": true
                },    
                .  
                .  
                .  
                .  
                ]
        }
    },
    .  
    .  
    .  
    .   
]        

```  



<br>  
<br>  

