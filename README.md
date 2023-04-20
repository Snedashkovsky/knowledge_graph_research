## Research of Knowledge Graphs 

### Install
[ClickHouse](https://clickhouse.tech/docs/en/getting-started/install/)

### Knowledge Graph sources
#### [CaLiGraph](http://caligraph.org/resources.html)  
- 125M links  
- 2 GB in Clickhouse  
- 20 GB in nt files  
- 1.3 GB in archive  
#### Wikidata
[Database download](https://www.wikidata.org/wiki/Wikidata:Database_download/en)  
[Dumps](https://dumps.wikimedia.org/wikidatawiki/entities/) (Truthy RDF file)
- 5,556M links
- 43 GB in Clickhouse  
- 41 GB in archive    

### Knowledge Graph processing
#### [Upload RDF standard Knowledge Graphs to Clickhouse (nt files)](upload_nt_to_ch.ipynb)
#### [Process Raw Knowledge Graphs in Clickhouse](process_raw_knowledge_graph_in_ch.ipynb)

### Bostrom 
#### Graph extraction
- install and synchronize [cyberindex](https://github.com/cybercongress/cyberindex)
- install postgresql client
```bash
sudo apt-get install postgresql-client
```
- connect to the Bostrom index database
```bash
psql --host=localhost --username=default --dbname=cyberd
```
- export data of the `cyberlink` table:
```sql
\copy cyberlink to 'cyberlink.csv' csv header
```

#### [Upload Knowledge Graph to Bostrom network](upload_knowledge_graph_to_bostrom.ipynb)

#### [Upload Content Type Subgraph](upload_content_type_subgraph.ipynb)