import psycopg2
import atexit
import logging

from psycopg2.extensions import register_adapter, AsIs
from singleton import Singleton


def adapt_list(list_value):
    return AsIs("'{" + ', '.join(f'"{v}"' for v in list_value) + "}'")


register_adapter(list, adapt_list)


class DB(metaclass=Singleton):
    def __init__(self, dbname, user, password, host='db', port='5432'):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS xtable (
            id BIGSERIAL PRIMARY KEY,
            states TEXT[] DEFAULT '{}',
            catgirl_nsfw BOOLEAN NOT NULL DEFAULT FALSE
            )
        """)
        self.conn.commit()
        atexit.register(self._del, self)

    def getById(self, field_name: str, id: int):
        try:
            self.cursor.execute(f"SELECT {field_name} "
                                f"FROM xtable WHERE id = {id}",
                                )
            res = self.cursor.fetchone()
            logging.info(f'RES:: {res}')
            return res[0] if res is not None else res
        except psycopg2.Error:
            # logging.info(e)
            return None

    def setById(self, id: int, **kwargs):
        req = f"INSERT INTO xtable " \
              f"(id, {', '.join(map(str, kwargs.keys()))}) " \
              f"VALUES " \
              f"(%s, %s) " \
              f"ON CONFLICT (id) DO UPDATE SET" \
              f" {''.join(f'{k} = EXCLUDED.{k}' for
                          k in map(str, kwargs.keys()))}"
        logging.info(f'COMMAND:: {req, (id, *kwargs.values())}')
        self.cursor.execute(req, (id, *list(kwargs.values())))
        self.conn.commit()

    def _del(self, p=None):
        logging.info("deletion")
        self.cursor.close()
        self.conn.close()
