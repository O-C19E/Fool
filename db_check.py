import sqlite3
import sys
from select import select

conn = sqlite3.connect("licenses.db")
cursor = conn.cursor()

if __name__ == "__main__":
    selection = int(input("[1] licenses \n[2] activation logs \nChoose the database: "))
    if selection == 1:
        for row in cursor.execute("SELECT * FROM licenses"):
            print(row)
    elif selection == 2:
        for row in cursor.execute("SELECT * FROM activation_logs"):
            print(row)
    else:
        print("Invalid Option")

    conn.close()
