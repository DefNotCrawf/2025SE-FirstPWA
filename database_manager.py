import sqlite3 as sql
import time


def listExtension():
    con = sql.connect(".database/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM extension").fetchall()
    con.close()
    return data


def insertContact(email, name):
    max_retries = 5
    retry_delay = 1  # in seconds
    retries = 0

    while retries < max_retries:
        try:
            con = sql.connect(".database/data_source.db")
            cur = con.cursor()
            cur.execute(
                "INSERT INTO contact_list (email, name) VALUES (?, ?)", (email, name)
            )
            con.commit()
            con.close()
            break  # Exit the loop if the operation is successful
        except sql.OperationalError as e:
            if "database is locked" in str(e):
                retries += 1
                time.sleep(retry_delay)
            else:
                raise  # Re-raise the exception if it's not a "database is locked" error
