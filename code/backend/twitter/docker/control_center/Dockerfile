FROM ubuntu:18.04
MAINTAINER Pedro Escaleira

# install some tools
RUN apt-get update
RUN apt install -y software-properties-common
RUN apt-get install -y tar git curl nano vim wget net-tools build-essential
RUN apt-get install -y python3.8 python3.8-dev python3.8-distutils python-distribute python3-pip python-pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.8 get-pip.py

WORKDIR /twitter

# copy rest files
COPY / .

# install requirements
RUN pip3.8 install --upgrade setuptools
RUN pip3.8 install --user -r requirements_cc.txt


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
CMD [ "python3.8", "start_cc.py" ]
