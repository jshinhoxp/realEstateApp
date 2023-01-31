import sqlite3

conn = sqlite3.connect("housingdata.db")
cur = conn.cursor