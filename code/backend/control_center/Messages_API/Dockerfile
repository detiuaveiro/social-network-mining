FROM python:latest

ADD mongo_api.py /
ADD rabbitmq.py /
ADD postgreSQL.py /
ADD PDP.py /
ADD PEP.py /
ADD policy_api.py /
ADD task.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "-u", "rabbitmq.py" ]