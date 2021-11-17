import psycopg2
from environs import Env
from os import getenv

env = Env()
env.read_env()


base_data = {
    'host': getenv('HOST'),
    'database': getenv('DATABASE'),
    'user': getenv('USER'),
    'password': getenv('PASSWORD')
}


def conn_cur():
    conn = psycopg2.connect(**base_data)

    cur = conn.cursor()
    
    return conn, cur


def close_and_commit(conn, cur):
    conn.commit()
    cur.close()
    conn.close()