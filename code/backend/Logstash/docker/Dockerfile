FROM docker.elastic.co/logstash/logstash:7.1.1

#Clean directories and files if there is any
RUN rm -rf /usr/share/logstash/db
RUN rm -f /usr/share/logstash/pipeline/logstash.conf
RUN rm -f /usr/share/logstash/postgresql-42.2.5.jar

#Create directories needed
RUN mkdir /usr/share/logstash/db

#Install required plugins
RUN /usr/share/logstash/bin/logstash-plugin install logstash-input-jdbc

#Add required files
ADD pipeline/ /usr/share/logstash/pipeline/
ADD config/ /usr/share/logstash/config/
ADD dependencies/postgresql-42.2.5.jar /usr/share/logstash/postgresql-42.2.5.jar

CMD ["/usr/share/logstash/bin/logstash"]