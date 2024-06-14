from database_scripts.schema import cur 

def get_users_info():
    cur.execute("SELECT * FROM combination")
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
