# Social Network Mining

Mining in Social Networks

Hoje em dia as redes sociais possuem um papel muito relevante da difusão da informação. Os seus utilizadores estão constantemente a fazer publicações sobre os mais variados assuntos desde trivialidades e acontecimentos do dia a dia, a assuntos de maior relevância como política e ciência. A circulação desta informação tem vindo a aumentar exponencialmente, assim como a complexa rede envolvida na propagação desta informação e como tal várias áreas de estudo estão a dedicar-se a resolução de problemas relacionados com este tema. Mais recentemente a temática das "fake news", noticias falsas como o nome indica, tornou-se um tópico mediático, fazendo a sua resolução um problema de grande interesse.

# Dashboard

Dashboard desenvolvida em React.

Créditos da template: https://www.creative-tim.com/product/now-ui-dashboard-react


# Instagram's Bot

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
 $ sudo systemctl enamble postgresql   
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
