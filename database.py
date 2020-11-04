import sqlite3

def exe_query(query, param=None):
    con_obj = sqlite3.connect('database.db')
    cursor = con_obj.execute(query, param or [])
    res = cursor.fetchall()
    con_obj.commit()
    con_obj.close()
    return res

def create_files_table():
    exe_query('''CREATE TABLE IF NOT EXISTS files(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        category TEXT,
        file_id TEXT UNIQUE
        )'''
    )

def create_users_table():
    exe_query('''CREATE TABLE IF NOT EXISTS users(
        user_id TEXT UNIQUE,
        user_status TEXT,
        is_admin INTEGER
        )'''
    )

con_obj = sqlite3.connect('database.db')
c = con_obj.cursor()
