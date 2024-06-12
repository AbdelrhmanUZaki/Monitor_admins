import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()


def create_db_tables():
    # Create a table
    cur.execute('''CREATE TABLE IF NOT EXISTS bot_users (
                    tele_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    username TEXT,
                    date TEXT NOT NULL,
                    current_step INTEGER
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS combination (
                    combination_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bot_user_id INTEGER NOT NULL,                    
                    admin_id INTEGER NOT NULL,
                    admin_name TEXT NOT NULL,                  
                    source_group_id INTEGER NOT NULL,
                    source_group_name TEXT NOT NULL,
                    destination_group_id INTEGER,
                    destination_group_name TEXT,
                    destination_thread_id INTEGER,
                    date TEXT NOT NULL 
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS tmp (
                    tele_id INTEGER PRIMARY KEY,
                    source_group_id INTEGER NOT NULL,
                    source_group_name TEXT NOT NULL
                )''')


def insert_in_combination_table(values):
    cur.execute('''INSERT INTO combination
                ( bot_user_id, admin_name, 
                 admin_id, source_group_id, source_group_name,
                 destination_group_id, destination_group_name,
                 destination_thread_id, date)
                VALUES (?,?,?,?,?,?,?,?,?)''', values)


def get_users_info():
    cur.execute("SELECT * FROM combination")
    # print(cur.fetchall())
    for item in cur.fetchall():
        print(item)


def get_source_info():
    cur.execute('''
    SELECT admin_id, source_group_id FROM combination
    ''')
    all_data = cur.fetchall()
    print(f"type of get_source_info\n{type(all_data)}")
    print(f"data of get_source_info\n{all_data}")


def get_destination_info(destination_group_id, destination_thread_id):
    cur.execute('''SELECT destination_group_id, destination_thread_id FROM combination
                WHERE admin_id = ? AND source_group_id = ?''',
                (destination_group_id, destination_thread_id))
    all_data = cur.fetchall()
    print(type(all_data))
    print(f"type of get_destination_info\n {type(all_data)}")
    print(f"data of get_destination_info\n {all_data}")
