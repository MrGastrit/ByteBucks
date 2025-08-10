import psycopg2
import os
from dotenv import load_dotenv

load_dotenv("important.env")


conn = psycopg2.connect(user=os.getenv("USER"), password=os.getenv("DB_PASS"), host="localhost", port="5432", database=os.getenv("DATABASE"))
cursor = conn.cursor()

#user balance
#
#
def get_balance(user_id):
    cursor.execute("SELECT balance FROM users WHERE id = %s", (user_id,))

    balance = cursor.fetchone()[0]
    return balance if balance else 0

def set_balance(user_id, balance):
    cursor.execute("UPDATE users SET balance = %s WHERE id = %s", (balance, user_id))
    conn.commit()



#daily time
#
#
def get_daily_time(user_id):
    cursor.execute("SELECT daily_next FROM users WHERE id = %s", (user_id,))

    daily_time = cursor.fetchone()[0]
    return daily_time

def set_daily_time(user_id, timestamp):
    cursor.execute("UPDATE users SET daily_next = %s WHERE id = %s", (timestamp, user_id))
    conn.commit()



#items
#
#
def get_items(user_id):
    cursor.execute("SELECT items FROM users WHERE id = %s", (user_id,))

    items = cursor.fetchone()[0]
    return items

def get_need_items(user_id, array: list):
    cursor.execute("SELECT items @> %s FROM users WHERE id = %s", (array, user_id,))

    items = cursor.fetchone()[0]
    return items


def add_item(user_id, item: str):
    cursor.execute("UPDATE users SET items = COALESCE(items, ARRAY[]::text[]) || %s WHERE id = %s", ([item], user_id))
    conn.commit()



#works
#
#
def get_job(user_id):
    cursor.execute("SELECT profession FROM users WHERE id = %s", (user_id,))

    profession = cursor.fetchone()[0]
    return profession

def set_job(user_id, profession: str):
    cursor.execute("UPDATE users SET profession = %s WHERE id = %s", (profession, user_id))
    conn.commit()



#on work
#
#
def set_on_work(user_id, work: bool):
    cursor.execute("UPDATE users SET on_work = %s WHERE id = %s", (work, user_id))
    conn.commit()

def is_on_work(user_id):
    cursor.execute("SELECT on_work FROM users WHERE id = %s", (user_id,))

    on_work = cursor.fetchone()[0]
    return on_work if on_work else False



#work time
#
#
def get_start_work(user_id):
    cursor.execute("SELECT start_work FROM users WHERE id = %s", (user_id,))

    start_work = cursor.fetchone()[0]
    return start_work if start_work else None

def set_start_work(user_id, timestamp):
    cursor.execute("UPDATE users SET start_work = %s WHERE id = %s", (timestamp, user_id))
    conn.commit()

def get_next_payment(user_id):
    cursor.execute("SELECT next_payment FROM users WHERE id = %s", (user_id,))

    next_payment = cursor.fetchone()[0]
    return next_payment if next_payment else None

def set_next_payment(user_id, timestamp):
    cursor.execute("UPDATE users SET next_payment = %s WHERE id = %s", (timestamp, user_id))
    conn.commit()