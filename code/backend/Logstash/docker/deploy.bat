::DELETE OLD DOCKER DIRECTORY
ssh alunos@redis-redesfis.5g.cn.atnog.av.it.pt "rm -rf docker"
::COPY NEW ONE
scp -r docker alunos@redis-redesfis.5g.cn.atnog.av.it.pt:/home/alunos
::GIVE THE SCRIPT EXECUTIO PERMISSIONS
ssh alunos@redis-redesfis.5g.cn.atnog.av.it.pt "chmod +x /home/alunos/docker/scripts/deploy-elastic.sh"
ssh alunos@redis-redesfis.5g.cn.atnog.av.it.pt "chmod +x /home/alunos/docker/scripts/deploy-logstash.sh"
::ACCESS INTO VM
ssh alunos@redis-redesfis.5g.cn.atnog.av.it.pt