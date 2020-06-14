from django.dispatch import receiver
from wrappers.postgresql_wrapper import signal, PostgresAPI
from api.cache_manager import cacheAPI
import logging

log = logging.getLogger('Signal Handler')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("signal.log", "a"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)

table_to_model = {
	'logs': 'Log',
	'policies': 'Policy',
	'tweets': 'TweetStats',
	'users': 'UserStats'
}


@receiver(signal, sender=PostgresAPI)
def postgres_update(sender, **kwargs):
	log.info("Updating cache")
	model_name = table_to_model[kwargs['table_name']]
	cacheAPI.update_per_table(model_name)
