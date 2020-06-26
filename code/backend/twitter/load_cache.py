import requests

import logging

log = logging.getLogger('Cache Loader')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("first_load_cache.log", "w"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)
BASE_URL = 'http://127.0.0.1:8000'


def load():
	urls = [
		"graphs/gen_stats_grouped/accumulative",
		"graphs/gen_stats_grouped/new",
		"graphs/user_tweets_stats_grouped/accumulative",
		"graphs/user_tweets_stats_grouped/new",
		"graphs/relations_stats_grouped/accumulative",
		"graphs/relations_stats_grouped/new"
	]

	for url in urls:
		for group_type in ['day', 'month', 'year']:
			path = f"{BASE_URL}/{url}/{group_type}"
			response = requests.get(path)
			if response.status_code == 200:
				log.info(f"{path} -> Success")
			else:
				log.error(f"{path} -> Error")


load()