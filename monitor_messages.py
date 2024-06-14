from database_scripts.schema import cur


def fetch_all_combinations():
    cur.execute("SELECT * FROM combination")
    data = cur.fetchall()
    return data
