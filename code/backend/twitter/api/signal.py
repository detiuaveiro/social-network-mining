from django.dispatch import receiver
from wrappers.postgresql_wrapper import signal as postgres_signal, PostgresAPI
from wrappers.neo4j_wrapper import signal as neo4j_signal, Neo4jAPI
from wrappers.mongo_wrapper import signal as mongo_signal, MongoAPI
import os
import logging
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
django.setup()

log = logging.getLogger('Signal Handler')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("signal.log", "a"))
handler.setFormatter(logging.Formatter(
    "[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)


@receiver(postgres_signal, sender=PostgresAPI)
def postgres_update(sender, **kwargs):
    from api.queries import update_per_table, cacheAPI
    log.info("Updating cache -> Postgres")
    update_per_table(cacheAPI, kwargs['table_name'])


@receiver(neo4j_signal, sender=Neo4jAPI)
def neo4j_update(sender, **kwargs):
    from api.queries import update_per_table, cacheAPI
    log.info("Updating cache -> Neo4j")
    update_per_table(cacheAPI, kwargs['table_name'])


@receiver(mongo_signal, sender=MongoAPI)
def mongo_update(sender, **kwargs):
    from api.queries import update_per_table, cacheAPI
    log.info("Updating cache -> Mongo")
    update_per_table(cacheAPI, kwargs['table_name'])
