FROM ubuntu
MAINTAINER Pedro Escaleira

# install some tools
RUN apt-get update
RUN apt-get install -y tar git curl nano vim wget net-tools build-essential
RUN apt-get install -y python3 python3-dev python-distribute python3-pip python-pip
RUN apt-get install -y tor

WORKDIR /twitter

# copy rest files
COPY / .

# install requirements
RUN pip3 install --upgrade setuptools
RUN pip3 install --user -r requirements_bot.txt


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
CMD [ "python3", "start_bot.py" ]
