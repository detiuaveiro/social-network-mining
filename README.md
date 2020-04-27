# Social Network Mining
 
Mining in Social Networks

Hoje em dia as redes sociais possuem um papel muito relevante da difusão da informação. Os seus utilizadores estão constantemente a fazer publicações sobre os mais variados assuntos desde trivialidades e acontecimentos do dia a dia, a assuntos de maior relevância como política e ciência. A circulação desta informação tem vindo a aumentar exponencialmente, assim como a complexa rede envolvida na propagação desta informação e como tal várias áreas de estudo estão a dedicar-se a resolução de problemas relacionados com este tema. Mais recentemente a temática das "fake news", noticias falsas como o nome indica, tornou-se um tópico mediático, fazendo a sua resolução um problema de grande interesse.

## Web App

Web app developed using the template: https://coreui.io/react/

To run, first install dependencies:
```
$ cd web-app
$ npm install
$ npm install @material-ui/core
$ npm install react-device-detect --save
$ npm install jquery
$ npm i react-countup
$ npm i react-visibility-sensor
$ npm i react-loading
$ npm i react-toastify
$ npm i react-graph-vis
$ npm i react-select
$ npm install react-paginate --save
```

Then use the command to start the web app on port 3000:
`$ npm start`

## Instagram's Bot

### Requirements:

1. instaloader
    

### Installation

`pip3 install -r requirements.txt `


### Usage

` python3 insta.py `


# Control Center
## Postgresql
### Istallation

| Arch Linux | Debian |
| ---------- | ------ |
| `sudo pacman -S postgresql` | `sudo apt update; sudo apt install postgresql postgresql-contrib`
 |

 ```bash
 $ sudo mkdir /var/lib/postgres/data
 $ sudo chown postgres /var/lib/postgres/data
 $ sudo -i -u postgres
 $ initdb  -D '/var/lib/postgres/data'
 $ sudo systemctl start postgresql
 ```

### Run database server and create credentials
 ```bash
 $ sudo su postgres -c psql
 ```
 ```postgres
 # CREATE USER postgres WITH PASSWORD 'password';
 # ALTER ROLE postgres WITH CREATEDB; 
 # CREATE DATABASE policies;
 # CREATE DATABASE postgres;
 ```

## Mongo
### Installation
| Arch Linux | Debian |
| ---------- | ------ |
| `yay mongo` | [tutorial](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

```bash
 $ sudo systemctl enable mongodb
```

### Run database server and create credentials
 ```bash
 $ mongo
 ```

## Neo4j
### Installation
| Arch Linux | Debian |
| ---------- | ------ |
| [tutorial](https://neo4j.com/developer/docker-run-neo4j/) | [tutorial](https://neo4j.com/docs/operations-manual/current/installation/linux/)

 - On Debian:
```bash
 $ sudo systemctl enable neo4j
```

 - On Arch Linux:
 ```bash
 $ docker run neo4j
 ```

### Run database server and create credentials
 ```bash
 $ neo4j console 
 $ cypher-shell            # to set new password
 ```

## Configure ToR (necessary on the deployment server and on the programmers machines)
 - Instalation and setting:
 ```bash
 $ sudo apt-get install tor         # instalation on Debian systems
 $ sudo pacman -S tor               # instalation on Arch systems
 $ sudo systemctl start tor         # on the deployment server is recomended to enable the service instead of starting it each time the machine boots
 ```

 - On the server side, it's necessary to run a new `tor` service for each new bot we have:
   - For each new bot, create a file /etc/tor/torrc.{1..<number of bots>} with the following content (note that it's necessary to change the ports for each new bot and the number on the directory). Then, on the bots, we have to connect to the port defined on `SocksPort`:
   ```
   SocksPort 9060
   ControlPort 9061
   DataDirectory /var/lib/tor1
   ```

 - On the server, it is necessary to run the bots with the environment variable `PROXY` with the proxy value (the default value is the localhost value)
 - More info about how to configure ToR with python on [link](https://medium.com/@jasonrigden/using-tor-with-the-python-request-library-79015b2606cb)


## Server Deploy
 - First, it's necessary to make a pull request to github with the tag `deploy` with the code we want to deploy next to the server. This will trigger the deploy workflow, that will create new images of the code to be deployed.
 - The first time, it's necessary to have all containers pre-created on the server. So, on the server terminal, run:
 ```bash
 $ docker container run --env-file ~/PI_2020/env_vars/rest.env --publish 7000:7000 --detach --name rest docker.pkg.github.com/detiuaveiro/social-network-mining/rest                # run the rest container
 $ docker container run --env-file ~/PI_2020/env_vars/bot.env --network host --detach --name bot docker.pkg.github.com/detiuaveiro/social-network-mining/bot                # run the bot container
 $ docker container run --env-file ~/PI_2020/env_vars/control_center.env --cpus=".7" --memory="12g" --detach --name control_center docker.pkg.github.com/detiuaveiro/social-network-mining/control_center               # run the control center container 
 ```
 - Also, it's necessary to have a `watchtower` container running on the server, that will deploy automaticly all the images created with the `deploy github workflow`:
 ```bash
 $ docker run --env-file PI_2020/env_vars/watchtower.env -d --name watchtower -v /var/run/docker.sock:/var/run/docker.sock -v ~/.docker/config.json:/config.json containrrr/watchtower
 ```

## BDS
- mongodb
```bash
mongoimport --db twitter --collection tweets --file scripts/mongodb/tweets.json -u user -p password
mongoimport --db twitter --collection users --file scripts/mongodb/users.json -u user -p password
```
- postgresql
```bash
psql -U postgres_pi twitter -h localhost < scripts/postgresql/twitter.pgsql 
```

- neo4j
```bash
  CALL apoc.load.json("user_nodes.json")
  YIELD value
  MERGE (p:User {name: value.a.properties.name, id: value.a.properties.id, username: value.a.properties.username})
```
```bash
  CALL apoc.load.json("bots_nodes.json")
  YIELD value
  MERGE (p:Bot {name: value.a.properties.name, id: value.a.properties.id, username: value.a.properties.username})
```
```bash
  CALL apoc.load.json("tweets.json")
  YIELD value
  MERGE (p:Tweet {id: value.a.properties.id})
```
```bash
  CALL apoc.load.json("follow_rel.json")
  YIELD value
  MATCH(p {id:value.start.properties.id})
  MATCH(u {id:toInteger(value.end.properties.id)})
  CREATE (p)-[:FOLLOWS]->(u)
```
```bash
  CALL apoc.load.json("retweet.json")
  YIELD value
  MATCH(p {id:value.start.properties.id})
  MATCH(u {id:toInteger(value.end.properties.id)})
  CREATE (p)-[:RETWEET]->(u)
```
```bash
  CALL apoc.load.json("reply.json")
  YIELD value
  MATCH(p {id:value.start.properties.id})
  MATCH(u {id:toInteger(value.end.properties.id)})
  CREATE (p)-[:REPLY]->(u)
```
```bash
  CALL apoc.load.json("wrote.json")
  YIELD value
  MATCH(p {id:value.start.properties.id})
  MATCH(u {id:toInteger(value.end.properties.id)})
  CREATE (p)-[:WROTE]->(u)
```
```bash
  CALL apoc.load.json("quote.json")
  YIELD value
  MATCH(p {id:value.start.properties.id})
  MATCH(u {id:toInteger(value.end.properties.id)})
  CREATE (p)-[:QUOTED]->(u)
```