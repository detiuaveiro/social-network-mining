FROM ubuntu
MAINTAINER Pedro Escaleira

# install some tools
RUN apt-get update
RUN apt-get install -y tar git curl nano vim wget net-tools build-essential
RUN apt-get install -y python3 python3-dev python-distribute python3-pip python-pip

WORKDIR /twitter

# copy rest files
COPY / .

# install requirements
RUN pip3 install --upgrade setuptools
RUN pip3 install --user -r requirements_bot.txt

CMD [ "python3", "start_cc.py" ]
