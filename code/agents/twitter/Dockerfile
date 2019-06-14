FROM python:3.7.3-alpine3.9

RUN mkdir -p /twitter_bots

WORKDIR /twitter_bots

COPY . /twitter_bots

RUN apk add rsyslog

# build dependencies, stored in a virtual package
RUN apk add --update --no-cache --virtual .build-dependencies \ 
	g++ python-dev libxslt-dev

# Runtime dependencies
RUN apk add --update --no-cache libxslt 

RUN pip install -r requirements.txt

# Removing the virtual package created
RUN apk del .build-dependencies

# Env variables used

ENV KEY

ENV SECRET

ENV TOKEN

ENV TOKEN_SECRET

ENV SERVER_HOST

ENV SERVER_PORT

# Don't use a proxy by default
ENV TOR_PROXY ""


# Add crontab file in the cron directory
COPY crontab /etc/crontab

# Give execution rights on the cron job
RUN chmod 0644 /etc/crontab

#Apply cron job
RUN crontab /etc/crontab

# Run the command on container startup
CMD crond -f && tail
