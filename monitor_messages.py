from database_scripts.schema import cur


def fetch_all_combinations(bot_user_id, bot_user_name):
    cur.execute("SELECT DISTINCT source_group_name, destination_group_name FROM combination WHERE bot_user_id = ?", (bot_user_id,))
    data = cur.fetchall()
    msg = f"مرحبا {bot_user_name}\n\n"
    msg += "المجموعات التي يتم متابعتها\n"
    for item in data:
        # item 0 -> Source Group Name
        # item 1 -> Destination Group Name
        msg += f"- {item[0]} => {item[1]}\n"
    return msg

def fetach_admin_ids(bot_user_id):
    pass
