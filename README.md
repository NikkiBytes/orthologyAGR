# Orthology AGR Data Plugin for BioThings   
  
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

## Notes    

- **Entity-Centric** document structure.  
<br>  

- **Asthetic("display") detail":** The variable, `"algorithms": "PhylomeDB|OrthoFinder|Hieranoid|OMA|Ensembl Compara|Roundup|InParanoid|PANTHER|OrthoInspector"` is available in the data file. Currently the created output document doesn't include it, but can easily be added. Note, if added, we considered reformatting the data string into a list.

<br>

- Need to translate to the NCBI gene ID on some of the given gene IDs. Some of the IDs aren't found using the mygene.info client search.  
    *A list is created to track what ids are not being found,*.  <br>   
    - The `'ZDB-GENE-*` IDs translated with reference from the [ZFIN Database](https://zfin.org/downloads).  
              File downloaded [ZFIN Marker associations to NCBI Gene data file]().  
      <br>

    - The `'SGD:S0*` IDs are the [SGD database]()
<br>  

  **Need to determine what the numeric IDs are**  

<br>  

- Confirmed the combinations of the relations. The **pairwise links** between the IDs was searched between `gene1ID` and `gene2ID` to confirm the ID pairwise exists
among groupings. Created document structure accordingly.  

  
<br>
