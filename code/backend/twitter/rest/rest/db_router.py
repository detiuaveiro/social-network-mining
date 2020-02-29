
# All lower case !!!!
DB_mapping = {
    'mongo': ['testmongo'],
    'postgres': ['testpostgres']
}


# Atenção esta função nunca pode retornar None, pois uma default DB não existe
def get_db(model_name):
    for db_name in DB_mapping:
        if model_name.lower() in DB_mapping[db_name]:
            return db_name


class DB_Router:
    def db_for_read(self, model, **hints):
        return get_db(model.__name__)

    def db_for_write(self, model, **hints):
        return get_db(model.__name__)

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return app_label != 'api' or db == get_db(model_name)
