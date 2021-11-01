# Orthology AGR Data Plugin for BioThings   
  
## <u> Document Structure </u>
      
```
{
{'_id': '176377',
  'agr': {'ortholog': {'geneid': 'SGD:S000003566',
    'symbol': 'VPS53',
    'taxid': 559292,
    'algorithmsmatch': 9,
    'outofalgorithms': 10,
    'isbestscore': True,
    'isbestrevscore': True}}}
```  



<br>  
<br>  

## Notes    
- The variable, `"algorithms": "PhylomeDB|OrthoFinder|Hieranoid|OMA|Ensembl Compara|Roundup|InParanoid|PANTHER|OrthoInspector"` is available in the data file. Currently the created output document doesn't include it, but can easily be added. Note, if added, we considered reformatting the data string into a list.

<br>

- translating the IDs to ncbi:gene id numeric: some data ids aren't found using the mygene.info client search.  
    A list has been created to track what ids are not being found. We see there is a pattern: <br>  

     ``` ['ZDB-GENE-041114-199', '1311391', '1915549', 'ZDB-GENE-070112-1002', '1586427', '2444430', 'ZDB-GENE-030131-260', 'ZDB-GENE-060929-828', 'ZDB-GENE-040426-2217', '621079', '620245', '2142527', '1566418', '1920462', 'ZDB-GENE-070209-131', 'ZDB-GENE-040426-1192', 'ZDB-GENE-050522-314', '1560053', '1563868', '2441730', '1336172', 'ZDB-GENE-040426-1869', 'ZDB-GENE-060616-266', 'ZDB-GENE-040718-60', 'ZDB-GENE-070424-85', '1589953', '1308104', '1303247', '2144766', '2145373', '2444911', '2147731', 'ZDB-GENE-030131-1394', 'ZDB-GENE-050809-111', '1306146', '2155936', 'ZDB-GENE-040122-2', 'ZDB-GENE-090313-225', 'ZDB-GENE-000831-3', '1195264', 'ZDB-GENE-050208-284', '1588894', '1914021', 'ZDB-GENE-061220-11', '1563497', '1351630', 'ZDB-GENE-030131-2768', 'ZDB-GENE-050522-302', '1310783', '1309128'] ```

  

     For the `'ZDB-GENE-*` genes, the ZFIN database references the ID we need. Looking for a file that references the ID, _webscraping is an option too...?_  

     **Need to determine the numeric IDs**  

<br>  

- verifying that `gene1id` and `gene2id` both reference eachother to confirm data document setup 
  
  
<br>
