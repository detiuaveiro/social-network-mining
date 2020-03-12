# Run Neo4j on docker

1. Pull a neo4j docker image - version 3.5.15 (it is not the latest because , openSSL gives error with latest version)
```
docker pull neo4j:3.5.15
```

2. Create neo4j volumes for docker
```
neo4j
    conf
    import
    plugins

mkdir ~/neo4j
mkdir ~/neo4j/conf
mkdir ~/neo4j/import
mkdir ~/neo4j/plugins
```

3. Download and move a apoc.jar to plugins folder ~/neo4j/plugins
- [Apoc.jar](https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/tag/3.5.0.9)

4. Download and move a neo4 config file to conf folder ~/neo4j/conf
- [neo4j config file](http://s000.tinyupload.com/index.php?file_id=06009987256241638153)

5. Run follow command 
```
docker run --name twitter_neo4j -p7474:7474 -p 7687:7687 -v $HOME/neo4j/plugins:/plugins  -v  $HOME/neo4j/conf:/conf  -v $HOME/neo4j/import:/import --user 1000:1000  neo4j:3.5.15 
```

6. Access to localhost:7474 and change password
- Default credentials
    - Username : neo4j
    - Password : neo4j


7. In case you run a export process using apoc, they will be written on ~/neo4j/import folder

# Convert neo4j bots string ids to Integer ids

```neo4j
MATCH (n:Bot) Set n.id = toInt(n.id)
```
