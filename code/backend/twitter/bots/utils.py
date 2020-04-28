import random
from datetime import datetime
import time
import json

import readtime


# -----------------------------------------------------------
# json
# -----------------------------------------------------------
from bots.settings import MAX_READ_TIME_RANDOM


def to_json(obj):
    return json.dumps(obj, separators=(',', ':'))


def from_json(string):
    return json.loads(string)


def current_time(str_time=False):
    if str_time:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return datetime.utcnow().timestamp()


def wait(seconds: float):
    time.sleep(seconds)


def virtual_read_wait(text: str) -> float:
    """Function to fake the reading time for the given text

    :param text: text to read
    :return: time taken to read the provided text
    """
    time_to_read = readtime.of_text(text).seconds
    wait(time_to_read*1.3)           # random.randint(1, MAX_READ_TIME_RANDOM)

    return time_to_read
