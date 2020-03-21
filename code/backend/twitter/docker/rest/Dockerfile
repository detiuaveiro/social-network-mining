FROM ubuntu
MAINTAINER Pedro Escaleira

# install some tools
RUN apt-get update
RUN apt-get install -y tar git curl nano vim wget net-tools build-essential tree
RUN apt-get install -y python3 python3-dev python-distribute python3-pip python-pip

WORKDIR /twitter

# install requirements
COPY requirements_rest.txt .
RUN pip3 install --upgrade setuptools
RUN pip3 install --user -r requirements_rest.txt

# copy rest files
COPY / .

EXPOSE 7000

# env variables
ENV MONGO_URL=$MONGO_URL
ENV MONGO_DB=$MONGO_DB
ENV MONGO_USERNAME=$MONGO_USERNAME
ENV MONGO_PASSWORD=$MONGO_PASSWORD

ENV POSTGRES_URL=$POSTGRES_URL
ENV POSTGRES_DB=$POSTGRES_DB
ENV POSTGRES_USERNAME=$POSTGRES_USERNAME
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD

ENV NEO4J_URL=$NEO4J_URL
ENV NEO4J_USERNAME=$NEO4J_USERNAME
ENV NEO4J_PASSWORD=$NEO4J_PASSWORD

# run
CMD [ "python3", "start_rest.py", "runserver", "7000" ]
