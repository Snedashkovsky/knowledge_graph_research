# Research of Knowledge Graphs 
## Install
[ClickHouse](https://clickhouse.tech/docs/en/getting-started/install/)
## Knowledge Graph sources
### [CaLiGraph](http://caligraph.org/resources.html)  
- 125M links  
- 2 GB in Clickhouse  
- 20 GB in nt files  
- 1.3 GB in archive  
### Wikidata
#### [Database download](https://www.wikidata.org/wiki/Wikidata:Database_download/en)  
#### [Dumps](https://dumps.wikimedia.org/wikidatawiki/entities/) (Truthy RDF file)
- 5,556M links
- 43 GB in Clickhouse  
- 41 GB in archive    
## Upload RDF standard Knowledge Graphs (nt files)
[jupyter notebook](upload_nt_to_ch.ipynb)
## Process Raw Knowledge Graphs in Clickhouse
[jupyter notebook](process_raw_knowledge_graph_in_ch.ipynb)