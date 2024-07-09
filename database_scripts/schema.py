from sqlite3 import connect


def create_db_tables():
    cur.execute(
        """CREATE TABLE IF NOT EXISTS bot_users (
                    tele_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    username TEXT,
                    date TEXT NOT NULL,
                    current_step INTEGER
                )"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS combination (
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
                )"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS tmp (
                    tele_id INTEGER PRIMARY KEY,
                    source_group_id INTEGER NOT NULL,
                    source_group_name TEXT NOT NULL
                )"""
    )


conn = connect("database.db")
cur = conn.cursor()
