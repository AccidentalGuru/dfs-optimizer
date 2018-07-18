import MySQLdb
import connection


def insert_qb_data(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc('insert_into_qb_table', data)
    cur.close()
    conn.commit()
    conn.close()

def insert_rb_data(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc('insert_into_rb_table', data)
    cur.close()
    conn.commit()
    conn.close()

def insert_wr_data(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc('insert_into_wr_table', data)
    cur.close()
    conn.commit()
    conn.close()

def insert_te_data(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc('insert_into_te_table', data)
    cur.close()
    conn.commit()
    conn.close()

def insert_defense_data(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc('insert_into_defense_table', data)
    cur.close()
    conn.commit()
    conn.close()

def insert_kicker_data(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc('insert_into_kicker_table', data)
    cur.close()
    conn.commit()
    conn.close()

def initialize_database():
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc('initialize_database')
    cur.close()
    conn.close()

def get_connection():
    return MySQLdb.connect(
        host=connection.host,
        user=connection.user,
        passwd=connection.passwd,
        db=connection.db)
