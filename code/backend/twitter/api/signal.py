from django.dispatch import receiver
from wrappers.postgresql_wrapper import signal, PostgresAPI
from api.cache_manager import cacheAPI


table_to_model = {
	'logs': 'Log',
	'policies': 'Policy',
	'tweets': 'TweetStats',
	'users': 'UserStats'
}


@receiver(signal, sender=PostgresAPI)
def postgres_update(sender, **kwargs):
	model_name = table_to_model[kwargs['table_name']]
	cacheAPI.update_per_table(model_name)
