# Migrate data on neo4j (docker)





1. Copy all content from  **social-network-mining/databases_and_rabbit_copy/neo4j** to a folder outside of project
``` 
$ mkdir ~/it_databases
$ cp -rf databases_and_rabbit_copy/neo4j ~/it_databases
```

2. Merge files chunks on neo4j data
```
$ cd ~/it_databases/neo4j/data/databases/graph.db
$ cat x* > neostore.transaction.db.0
```

3. Download a neo4j docker images
```
$ docker pull neo4j:3.5.15
```

4. Run following command
```
$ cd ~/it_databases
$ sudo chown -R 1000:1000 neo4j
$ docker run --name it_twitter_neo4j -p7474:7474 -p7687:7687 -v $HOME/it_databases/neo4j/data:/data -v $HOME/it_databases/neo4j/logs:/logs -v $HOME/it_databases/neo4j/plugins:/plugins -v $HOME/it_databases/neo4j/conf:/conf -v $HOME/it_databases/neo4j/import:/import --user 1000:1000 neo4j:3.5.15
```

 - Access to (link)[http://localhost:7474/] and introduce the credentials:
   - User: `neo4j`
   - Password: `neo4jPI`
