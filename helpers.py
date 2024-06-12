from pyrogram.types import ChatMember, Message, ForumTopicCreated
from pyrogram import enums
from pyrogram.filters import new_chat_members
from config import app, get_bot_id
from db import conn, cur, insert_in_combination_table


def add_user_if_not_exists(user_id, name, user_username, user_joined_date):
    # Check if the user already exists in the database
    cur.execute("SELECT * FROM bot_users WHERE tele_id = ?", (user_id,))
    existing_user = cur.fetchone()

    if not existing_user:
        # New user
        current_step = 1  # will add first group now (the source group) 
        cur.execute("INSERT INTO bot_users (tele_id, name, username, date, current_step) VALUES (?, ?, ?, ?, ?)",
                    (user_id, name, user_username, user_joined_date, current_step))
        conn.commit()


@app.on_message(new_chat_members)
async def on_join(client, message: Message):
    cur.execute("SELECT current_step FROM bot_users WHERE tele_id = ?", (message.from_user.id,))
    current_step = cur.fetchone()[0]
    if current_step == 1:
        await step_1(message)
    elif current_step == 2:
        await step_2(message)

async def step_1(message):
    """
    The bot has been added to the first group (Source group)
    """
    bot_id = await get_bot_id()
    if message.new_chat_members and bot_id in [member.id for member in message.new_chat_members]:
        await get_source_chat_id(message)
        # with source_chat_id I could get the source group admins
    
async def step_2(message):
    """
    The bot has been added to the second group (Destination group)
    """
    destination_group_id = message.chat.id
    destination_group_name = message.chat.title
    user_id = message.from_user.id
    source_group_id, source_group_name = await get_source_group_info(user_id)
    async for admin in app.get_chat_members(source_group_id,
                                            filter=enums.ChatMembersFilter.ADMINISTRATORS):
        admin: ChatMember
        if admin.user.is_bot is False:
            admin_id = admin.user.id
            admin_name = admin.user.full_name
            chat_id = message.chat.id
            topic_id = await get_topic_id(chat_id, admin_name)
            values = (message.from_user.id, admin_name, admin_id,
                      source_group_id, source_group_name,
                      destination_group_id, destination_group_name,
                      topic_id, message.date)
            insert_in_combination_table(values)
    conn.commit()
    # await set_current_admins_chat_id_null(user_id)


async def get_topic_id(chat_id, admin_name):
    topic_created = await app.create_forum_topic(chat_id, f"{admin_name}")
    return topic_created.id


async def get_source_group_info(user_id):
    cur.execute("SELECT source_group_id, source_group_name from tmp WHERE tele_id = ?", (user_id, ))
    all_data = cur.fetchall()[0]
    source_group_id = all_data[0]
    source_group_name = all_data[1]
    return source_group_id, source_group_name


async def get_source_chat_id(source_message: Message):
    """
    This to get the message that contain admins
    """
    bot_user_id = source_message.from_user.id
    source_group_id = source_message.chat.id
    source_group_name = source_message.chat.title
    msg = f"Source group that will be monitoring {source_message.chat.title}"
    cur.execute("INSERT INTO tmp values(?,?,?)", (bot_user_id,
                                                  source_group_id,
                                                  source_group_name))
    conn.commit()
    await app.send_message(source_message.from_user.id, msg)
    await update_current_step(source_message.from_user.id)


async def update_current_step(user_id):
    msg = f'Now add the destination group\n\n'
    msg += f'Note: Destination group must be in "Topics" view, enable it from group settings first\n\n'
    await app.send_message(user_id, msg)
    cur.execute("UPDATE bot_users SET current_step = 2 WHERE tele_id = ?", (user_id,))
    conn.commit()
