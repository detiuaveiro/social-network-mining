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


## Server Deploy
 - First, it's necessary to make a pull request to github with the tag `deploy` with the code we want to deploy next to the server. This will trigger the deploy workflow, that will create new images of the code to be deployed.
 - The first time, it's necessary to have all containers pre-created on the server. So, on the server terminal, run:
 ```bash
 $ docker container run --env-file ~/PI_2020/env_vars/rest.env --publish 7000:7000 --detach --name rest docker.pkg.github.com/detiuaveiro/social-network-mining/rest                # run the rest container
 $ docker container run --env-file ~/PI_2020/env_vars/bot.env --detach --name bot docker.pkg.github.com/detiuaveiro/social-network-mining/bot                # run the bot container
 $ docker container run --env-file ~/PI_2020/env_vars/control_center.env --detach --name control_center docker.pkg.github.com/detiuaveiro/social-network-mining/control_center                # run the control center container
 ```
 - Also, it's necessary to have a `watchtower` container running on the server, that will deploy automaticly all the images created with the `deploy github workflow`:
 ```bash
 $ docker run --env-file PI_2020/env_vars/watchtower.env -d --name watchtower -v /var/run/docker.sock:/var/run/docker.sock -v ~/.docker/config.json:/config.json containrrr/watchtower
 ```

