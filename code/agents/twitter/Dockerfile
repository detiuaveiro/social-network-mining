FROM ubuntu:latest

ADD requirements.txt /
ADD cache.py /
ADD enums.py /
ADD exceptions.py /
ADD models.py /
ADD settings.py /
ADD twitter_bot.py /
ADD utils.py /
ADD crontab /

RUN apt-get update \
  && apt -y install software-properties-common \
  && add-apt-repository -y ppa:deadsnakes/ppa \
  && apt -y install python3.7 \
  && apt -y install curl \
  && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && python3.7 get-pip.py \
  && apt-get -y install cron 

RUN apt-get install -y rsyslog

RUN pip install -r requirements.txt

# Add crontab file in the cron directory
COPY crontab /etc/crontab

# Give execution rights on the cron job
RUN chmod 0644 /etc/crontab

#Apply cron job
RUN crontab /etc/crontab
# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
