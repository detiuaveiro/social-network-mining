FROM python:3.7-alpine
COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN mkdir -p /bots
COPY . /bots
WORKDIR /bots
CMD python start_bot.py