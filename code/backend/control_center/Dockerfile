FROM python:latest

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY ./Mongo /Mongo
COPY ./Postgres /Postgres
COPY ./Neo4j /Neo4j
COPY ./Enums /Enums
COPY ./ElasticSearch /ElasticSearch
COPY send.py /
COPY settings.py /
COPY api.py /


EXPOSE 5000

CMD [ "python", "./api.py" ]