"""
    key: db name (defined on settings.py - DATABASES)
    value: List of model name you want to assign to a db (name of classes in models.py)

    Ex :
    {
    'mongo' : ['test']
    }
    'test' model object will be assigned to mongo database
    Whenever you write or read a test model object , this will be saved or read on mongo db
"""
# All lower case !!!!
DB_mapping = {
    'mongo': ['tweet', 'user'],
    'postgres': ['policy', 'userstats', 'tweetstats']
}


def get_db(model_name):
    """
    Given a model_name return the name of the corresponding database (definied by DB_mapping dictionary)

    :param model_name: currrent model_name
    :return: DB_name (string)
    """
    for db_name in DB_mapping:
        if model_name.lower() in DB_mapping[db_name]:
            return db_name
    # Should never return None!


class DB_Router:
    """
        A router to control all database operations on models
    """

    def db_for_read(self, model, **hints):
        """
        Suggest the database that should be used for read operations for objects of type model.

        :param model: model Object
        :param hints: used by certain operations to communicate additional information to the router
        :return: DB_name (string) or None(no suggestion)
        """
        return get_db(model.__name__)

    def db_for_write(self, model, **hints):
        """
        Suggest the database that should be used for writes of objects of type Model.

        :param model: model Object
        :param hints: used by certain operations to communicate additional information to the router
        :return: DB_name (string) or None(no suggestion)
        """
        return get_db(model.__name__)

    def allow_relation(self, obj1, obj2, **hints):
        """
        Return True if a relation between obj1 and obj2 should be allowed, False if the relation should be prevented, 
            or None if the router has no opinion.
        This is purely a validation operation, used by foreign key and many to many operations to determine if a 
            relation should be allowed between two objects.
        Decide if relation between 2 models from 2 differents database can interact through a relation

        :param obj1: model Object
        :param obj2: model Object
        :param hints: used by certain operations to communicate additional information to the router
        :return: Boolean or None
        """
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Determine if the migration operation is allowed to run on the database with alias db
        Return True if the operation should run, False if it shouldn’t run, or None if the router has no opinion.
        :param db: database alias
        :param app_label:  label of the application being migrated
        :param model_name: current model_name
        :param hints: used by certain operations to communicate additional information to the router
        :return: Boolean or None
        """
        # return app_label != 'api' or db == get_db(model_name)
        if db is None:
            return False
        return model_name is not None and db == get_db(model_name)
