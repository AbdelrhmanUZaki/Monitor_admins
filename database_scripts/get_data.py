from database_scripts.schema import cur


def fetch_all_combinations(bot_user_id, bot_user_name):
    cur.execute(
        "SELECT DISTINCT source_group_name, destination_group_name FROM combination WHERE bot_user_id = ?",
        (bot_user_id,),
    )
    data = cur.fetchall()
    msg = f"مرحبا {bot_user_name}\n\n"
    msg += "المجموعات التي يتم متابعتها\n"
    for item in data:
        # item 0 -> Source Group Name
        # item 1 -> Destination Group Name
        msg += f"- {item[0]} => {item[1]}\n"
    return msg


def fetch_all_db_admin_ids():
    # Example data structure
    # data = {
    #    'admin_id_1': {
    #        'source_group_id_1': ('destination_group_id_1', 'destination_thread_id_1'),
    #        'source_group_id_2': ('destination_group_id_2', 'destination_thread_id_2'),
    #        'source_group_id_3': ('destination_group_id_3', 'destination_thread_id_3')
    #    },
    #    'admin_id_2': {
    #        'source_group_id_4': ('destination_group_id_4', 'destination_thread_id_4'),
    #        'source_group_id_5': ('destination_group_id_5', 'destination_thread_id_5')
    #    },
    # }
    admins_mapping = {}
    cur.execute(
        "SELECT admin_id, source_group_id, destination_group_id, destination_thread_id from combination"
    )
    admins_fetched = cur.fetchall()
    for (
        admin_id,
        source_group_id,
        destination_group_id,
        destination_thread_id,
    ) in admins_fetched:
        if admin_id not in admins_mapping:
            admins_mapping[admin_id] = {}
        admins_mapping[admin_id][source_group_id] = (
            destination_group_id,
            destination_thread_id,
        )
    return admins_mapping


def get_source_info():
    cur.execute(
        """
    SELECT admin_id, source_group_id FROM combination
    """
    )
    all_data = cur.fetchall()
    print(f"type of get_source_info\n{type(all_data)}")
    print(f"data of get_source_info\n{all_data}")


def get_destination_info(destination_group_id, destination_thread_id):
    cur.execute(
        """SELECT destination_group_id, destination_thread_id FROM combination
                WHERE admin_id = ? AND source_group_id = ?""",
        (destination_group_id, destination_thread_id),
    )
    all_data = cur.fetchall()
    print(type(all_data))
    print(f"type of get_destination_info\n {type(all_data)}")
    print(f"data of get_destination_info\n {all_data}")
