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
RUN pip3.8 install --user -r requirements_fs.txt


# run
CMD [ "python3.8", "start_fs.py" ]
