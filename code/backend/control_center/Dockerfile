FROM python:latest

ADD api.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "./api.py" ]