FROM python:3.7-alpine
MAINTAINER miguel.fradinho <miguel.fradinho@ua.pt>
# needed for the requirements
RUN apk add --update --no-cache g++ gcc libxslt-dev

COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN mkdir -p /bots
COPY . /bots
WORKDIR /bots

# Executing the bots
CMD python twitter_bot.py

