import psycopg2
from src import settings


class EndpointRespository:
    """
    Establishes connection with the DB and returns the connection object
    """

    def __init__(self):
        self.conn = psycopg2.connect(settings.DB_URI)
        self.cur = self.conn.cursor()
        self.set_up()

    def set_up(self):
        """
        Creates two tables
        """

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS websites (url VARCHAR(255) NOT NULL,\
                 id SERIAL PRIMARY KEY);"
        )
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS status (website_id integer REFERENCES\
                 websites (id), status integer NOT NULL, ts TIMESTAMP\
                      NOT NULL);"
        )
        self.conn.commit()

    def do_commit(self):
        self.conn.commit()
