import requests
import os
import logging

log = logging.getLogger('Cache Loader')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("first_load_cache.log", "w"))
handler.setFormatter(logging.Formatter(
    "[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)
BASE_URL = os.environ.get('REST_URL', 'http://192.168.85.60:7000')


def load():
    urls_grouped_info = [
        "graphs/gen_stats_grouped/accumulative",
        "graphs/gen_stats_grouped/new",
        "graphs/user_tweets_stats_grouped/accumulative",
        "graphs/user_tweets_stats_grouped/new",
        "graphs/relations_stats_grouped/accumulative",
        "graphs/relations_stats_grouped/new",
    ]

    urls = [
        "graphs/general/today/",
        "graphs/user_tweets/today/",
        "graphs/relations/today/",
        "graphs/latest_tweets/daily/5/1",
        "graphs/latest_activities/daily/6/1",
        "graphs/latest_tweets/100/5/1/",
        "graphs/latest_activities/100/6/1/",
        "entities/counter"
    ]

    for url in urls_grouped_info:
        for group_type in ['day', 'month', 'year']:
            path = f"{BASE_URL}/{url}/{group_type}"
            response = requests.get(path)
            if response.status_code == 200:
                log.info(f"{path} -> Success")
            else:
                log.error(f"{path} -> Error")

    for url in urls:
        path = f"{BASE_URL}/{url}"
        response = requests.get(path)
        if response.status_code == 200:
            log.info(f"{path} -> Success")
        else:
            log.error(f"{path} -> Error")


if __name__ == '__main__':
    load()
