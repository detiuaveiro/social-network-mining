cd "/home/alunos/docker"
docker stop logstash
docker rm logstash
docker image rm logstash:latest
docker build --tag logstash ../
docker run -d --name logstash logstash:latest