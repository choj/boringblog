import sqlite3
con = sqlite3.connect('boring.db') # Warning: This file is created in the current directory

con.execute("CREATE TABLE user (id INTEGER PRIMARY KEY, email TEXT NOT NULL, join_date TEXT NOT NULL, last_login TEXT NOT NULL, blog_title TEXT NOT NULL, password_hash TEXT NOT NULL)")

con.commit()
