from config import app, get_bot_id
from database_scripts.get_data import fetch_all_db_admin_ids
from database_scripts.schema import conn, cur
from database_scripts.set_data import insert_in_combination_table
from pyrogram import enums
from pyrogram import filters
from pyrogram.types import ChatMember, Message, ForumTopicCreated

admins_mapping = {}

def add_new_user(user_id, name, user_username, user_joined_date):
    # Check if the user already exists in the database
    cur.execute("SELECT * FROM bot_users WHERE tele_id = ?", (user_id,))
    existing_user = cur.fetchone()

    if not existing_user:
        current_step = 1  # will add first group now (the source group) 
        cur.execute("INSERT INTO bot_users (tele_id, name, username, date, current_step) VALUES (?, ?, ?, ?, ?)",
                    (user_id, name, user_username, user_joined_date, current_step))
        conn.commit()

@app.on_message(filters.new_chat_members)
async def on_join(client, message: Message):
    """
    To know when bot is added into a new group
    """
    cur.execute("SELECT current_step FROM bot_users WHERE tele_id = ?", (message.from_user.id,))
    current_step = cur.fetchone()[0]
    if current_step == 1:
        await add_source_group(message)
    elif current_step == 2:
        await add_destinatin_group(message)

async def add_source_group(message):
    """
    The bot has been added to the first group (Source group)
    """
    bot_id = await get_bot_id()
    if message.new_chat_members and bot_id in [member.id for member in message.new_chat_members]:
        await get_source_chat_id(message)
        # with source_chat_id I could get the source group admins
    
async def add_destinatin_group(message):
    """
    The bot has been added to the second group (Destination group)
    """
    destination_group_id = message.chat.id
    destination_group_name = message.chat.title
    user_id = message.from_user.id
    source_group_id, source_group_name = await get_source_group_info(user_id)
    await get_group_admins(message, destination_group_id, destination_group_name, source_group_id, source_group_name)
    reset_current_step(message.from_user.id)
    reset_tmp_table(message.from_user.id)

def reset_current_step(tele_id):
    """
    Reset current_step to let user add another combinations as he need. 
    """
    current_step = 1  # 
    cur.execute("UPDATE bot_users SET current_step = ? WHERE tele_id = ?", (current_step, tele_id))
    conn.commit()

def reset_tmp_table(tele_id):
    cur.execute("DELETE FROM tmp WHERE tele_id = ?", (tele_id,))
    conn.commit()

async def get_group_admins(message, destination_group_id, destination_group_name, source_group_id, source_group_name):
    global admins_mapping 
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
    await inform_about_new_combination(message, source_group_name, destination_group_name)
    admins_mapping = fetch_all_db_admin_ids()

@app.on_message(filters.group)
async def forward_admin_messages(client, message: Message):
    global admins_mapping
    if message.from_user.id in admins_mapping and message.chat.id in admins_mapping[message.from_user.id]:
        destination_info = admins_mapping[message.from_user.id][message.chat.id]
        destination_group_id = destination_info[0]
        destination_thread_id = destination_info[1]
        await message.forward(destination_group_id, destination_thread_id)

async def inform_about_new_combination(message, source_group_name, destination_group_name):
    """
    Inform user about his new (source -> group combination)
    """
    msg = "مبارك!\n\nلقد قمت بربط مجموعتين جديدتين بنجاح.\n"
    msg += f"سيقوم البوت بتحويل الرسائل من '{source_group_name}' إلى '{destination_group_name}'.\n\nاضغط /list لعرض جميع المجموعات المتاحة" 
    msg += "\n\nلاستخدام البوت مرة أخرى يمكنك تكرار نفس الخطوات بداية من إضافة المجموعة الأولى ثم الثانية... إلخ)"
    await app.send_message(message.from_user.id, msg)

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
    msg = f"أحسنت!\nسيتابع البوت مجموعة '{source_message.chat.title}' على مدار الساعة."
    cur.execute("INSERT INTO tmp values(?,?,?)", (bot_user_id,
                                                  source_group_id,
                                                  source_group_name))
    conn.commit()
    await app.send_message(source_message.from_user.id, msg)
    await update_current_step(source_message.from_user.id)

async def update_current_step(user_id):
    msg = f"الآن أضف المجموعة التي تريد تحويل الرسائل إليها\n\n"
    msg += f"لاحظ أن: المجموعة المستهدفة يجب أن تكون في وضع التبويبات 'Topics'، لذا قم بتفعيلها من الإعدادات أولا"
    await app.send_message(user_id, msg)
    cur.execute("UPDATE bot_users SET current_step = 2 WHERE tele_id = ?", (user_id,))
    conn.commit()
