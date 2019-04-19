FROM python:latest

ADD mongo_api.py /
ADD rabbitmq.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "./rabbitmq.py" ]