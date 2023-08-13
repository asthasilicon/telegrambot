import sqlite3


conn = sqlite3.connect("database.db")

with open("D:\pythonProject\current\create_database.sql", "r") as f:
    sql = f.read()

conn.executescript(sql)


conn.commit()
conn.close()


