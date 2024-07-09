from database_scripts.schema import cur


def insert_in_combination_table(values):
    cur.execute(
        """INSERT INTO combination
                ( bot_user_id, admin_name, 
                 admin_id, source_group_id, source_group_name,
                 destination_group_id, destination_group_name,
                 destination_thread_id, date)
                VALUES (?,?,?,?,?,?,?,?,?)""",
        values,
    )
