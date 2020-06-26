FROM ubuntu:18.04
MAINTAINER Pedro Escaleira

# install some tools
RUN apt-get update
RUN apt install -y software-properties-common
RUN apt-get install -y tar git curl nano vim wget net-tools build-essential
RUN apt-get install -y python3.8 python3.8-dev python3.8-distutils python-distribute python3-pip python-pip python3-virtualenv
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.8 get-pip.py


WORKDIR /ParlAI

COPY / .

# install requirements
RUN pip3 install --upgrade setuptools
RUN pip3 install --user -r requirements.txt


EXPOSE 5555

# run
CMD python3.8 examples/remote.py \
    --remote-host \
    -m transformer/polyencoder \
    -mf zoo:pretrained_transformers/model_poly/model \
    --encode-candidate-vecs true \
    --eval-candidates fixed  \
    --fixed-candidates-path data/models/pretrained_transformers/tweets.txt
