FROM python:3.7.3-alpine3.9

RUN mkdir -p /twitter_bots

WORKDIR /twitter_bots

# Cron dependency
RUN apk add rsyslog

COPY requirements.txt /twitter_bots

# build dependencies, stored in a virtual package
RUN apk add --update --no-cache --virtual .build-dependencies \ 
	g++ \ 
	python-dev \ 
	libxslt-dev \
	# Runtime dependencies
	&& apk add --update --no-cache libxslt \
	&& pip install -r requirements.txt \
	&& apk del .build-dependencies

# Add crontab file in the cron directory
COPY crontab /etc/crontab

COPY *.py /twitter_bots/

COPY ./user_agents.json /twitter_bots/

# Give execution rights on the cron job
RUN chmod 0644 /etc/crontab \
	#Apply cron job
	&& crontab /etc/crontab

# Run the command on container startup
CMD crond -f && tail
