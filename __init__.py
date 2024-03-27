import sqlite3

CONN = sqlite3.connect('database.db')
CURSOR = CONN.cursor()