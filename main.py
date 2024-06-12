from config import app
from pyrogram.types import Message 
from pyrogram import filters
from helpers import on_join, add_user_if_not_exists
from db import create_db_tables


@app.on_message(filters.command(["start"]))
async def handle_message(client, message: Message):
    user_id = message.from_user.id
    name = message.from_user.full_name
    user_username = message.from_user.username
    user_joined_date = message.date
    add_user_if_not_exists(user_id, name, user_username, user_joined_date)

    msg = f"Hello {message.from_user.full_name}"
    msg += "\nFirst add this bot as an admin in the first group"
    msg += "\nNote: You shouldn't be hidden in that group"
    await message.reply(msg, reply_to_message_id=message.id)


if __name__ == "__main__":
    create_db_tables()
    app.run()
