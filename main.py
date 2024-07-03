from config import app
from database_scripts.get_data import fetch_all_combinations
from database_scripts.schema import create_db_tables
from helpers import on_join, add_new_user
from pyrogram import filters
from pyrogram.types import Message 

@app.on_message(filters.command(["start"]))
async def handle_message(client, message: Message):
    user_id = message.from_user.id
    name = message.from_user.full_name
    user_username = message.from_user.username
    user_joined_date = message.date
    add_new_user(user_id, name, user_username, user_joined_date)

    msg = f"مرحبا {message.from_user.full_name}\n\n"
    msg += "لبدء استخدام البوت قمت بإضافته للمجموعة الأولى (التي تريد متابعتها)\n"
    msg += "لاحظ أن: يجب أن لا تكون أنت كمشرف مخفيا.\nأي لا تقم بتفعيل هذا الخيار Remain anonymous في صلاحياتك كمشرف -على الأقل حتى تربط المجموعتين-."
    await message.reply(msg, reply_to_message_id=message.id)

@app.on_message(filters.command(['list', 'عرض']))
async def get_combinations(client, message: Message):
    """
    Fetach all combinations for that admin
    """
    msg = fetch_all_combinations(message.from_user.id, message.from_user.full_name)
    await message.reply(msg, reply_to_message_id=message.id)

#@app.on_message(filters.command(['help', 'مساعدة']))
#async def get_combinations(client, message: Message):
#    """
#    Show help message
#    """
#    msg = ''
#    await message.reply(msg, reply_to_message_id=message.id)


if __name__ == "__main__":
    create_db_tables()
    app.run()
