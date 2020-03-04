import psycopg2
import logging
import sys

sys.path.append("..")
import credentials

log = logging.getLogger("PostgreSQL")
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s")
)
log.addHandler(handler)


class PostgresAnalysisAPI:
    """PostgreSQL

    Encompasses methods used for all API and PDP interactions with our PostgreSQL DB.
    Interacts with the snm_analysis_pg (for time series analysis) database
    """

    def __init__(self):
        log.debug("Connecting to PostgreSQL Analysis")
        try:
            # Connect to the PostgreSQL server
            self.conn = psycopg2.connect(host=credentials.POSTGRES_URL, database="snm_analysis_pg",
                                         user=credentials.POSTGRES_USERNAME, password=credentials.POSTGRES_PASSWORD)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


class PostgresPoliciesAPI:
    """PostgreSQL

    Encompasses methods used for all API and PDP interactions with our PostgreSQL DB.
    Interacts with the snm_policies_pg (for bots' policies and PDP queries) database
    """

    def __init__(self):
        log.debug("Connecting to PostgreSQL Policies")
        try:
            # Connect to the PostgreSQL server
            self.conn = psycopg2.connect(host=credentials.POSTGRES_URL, database="snm_policies_pg",
                                         user=credentials.POSTGRES_USERNAME, password=credentials.POSTGRES_PASSWORD)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
