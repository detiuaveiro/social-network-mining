FROM ubuntu:18.04
MAINTAINER Pedro Escaleira

# install some tools
RUN apt-get update
RUN apt install -y software-properties-common
RUN apt-get install -y tar git curl nano vim wget net-tools build-essential
RUN apt-get install -y python3.8 python3.8-dev python3.8-distutils python-distribute python3-pip python-pip
RUN apt-get install -y tor
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.8 get-pip.py

WORKDIR /twitter

# copy rest files
COPY / .

# install requirements
RUN pip3.8 install --upgrade setuptools
RUN pip3.8 install --user -r requirements_bot.txt


# env variables
ENV RABBITMQ_URL=$RABBITMQ_URL
ENV RABBITMQ_USERNAME=$RABBITMQ_USERNAME
ENV RABBITMQ_PASSWORD=$RABBITMQ_PASSWORD

ENV BOT_ID=$BOT_ID
ENV CONSUMER_KEY=$CONSUMER_KEY
ENV CONSUMER_SECRET=$CONSUMER_SECRET
ENV TOKEN=$TOKEN
ENV TOKEN_SECRET=$TOKEN_SECRET

# run 
CMD [ "python3.8", "start_bot.py" ]
