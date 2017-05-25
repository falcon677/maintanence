import os
import json
import datetime
import sys
import MySQLdb
import MySQLdb.cursors
import ConfigParser
import logging
from contextlib import contextmanager
from  migrate_log import LOG

CONF = ConfigParser.ConfigParser()

cur_dir = os.path.split(os.path.realpath(__file__))[0]
CONFIG_FILE = os.sep.join([cur_dir, 'config.ini'])


def get_mysql_config(db_opt):
    CONF.read(CONFIG_FILE)
    DB_CONFIG  = dict(CONF.items(db_opt))
    return DB_CONFIG


class db_client(object):

    def __init__(self):
        self.source_conf = get_mysql_config('source')
        self.destination_conf = get_mysql_config('destination')

    @contextmanager
    def _get_conn(self, db_conf):
        try:
            conn = MySQLdb.connect(**db_conf)
            if conn:
                cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                yield cursor
        except Exception as e:
            LOG.error("Connect to db: failed, please check config file!")
            LOG.error(e)
            conn.rollback()
            raise e
        else:
            conn.commit()
            cursor.close()
            conn.close()
        finally:
            pass

    def execute_query(self, db_opt, sql, args=None, fetchall=False):
        res = None
        with self._get_conn(db_opt) as cursor:
            try:
                cursor.execute(sql)
                res = cursor.fetchall() if fetchall else cursor.fetchone()
            except Exception as ex:
                LOG.error('execute_query Error: %s', ex)
                raise ex
        return res

    def execute_insert(self, db_opt, sql, args=None):
        with self._get_conn(db_opt) as cursor:
            try:
                cursor.execute(sql, args)
            except Exception as ex:
                LOG.error('dst_execute_insert Error: %s' , ex)
                raise ex

    def exec_insert_dict(self, db_opt, table, my_dict):

        qmarks = ', '.join(['%s'] * len(my_dict))
        cols = '`, `'.join(my_dict.keys())
        cols = '`' + cols + '`'

        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, qmarks)
        with self._get_conn(db_opt) as cursor:
            try:
                cursor.execute(sql, my_dict.values())
            except Exception as ex:
                LOG.error('dst_execute_insert Error: %s', ex)
                raise ex


if __name__ == "__main__":
    db_client = db_client()
    sql = "select * from glance.images where id=%s;"
    image = '67963278-856e-46b7-a7c9-3d3850245b8a'
    res = db_client.execute_query(db_client.source_conf, sql, image)
    print res
