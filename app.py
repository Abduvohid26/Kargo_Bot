from loader import bot, db
import json
import logging
from json_writer_to_datase import json_writer_to_database  # Adjust with actual module name
import handlers, middlewares
from loader import dp, bot, db
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats
import asyncio
from utils.notify_admins import start, shutdown
from utils.set_botcommands import commands
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats(type='all_private_chats'))
        dp.startup.register(start)
        dp.shutdown.register(shutdown)

        # Create tables and import data
        try:
            db.create_table_users()
            db.create_table_address()
            db.create_table_orders()
            # json_writer_to_database()
            write_to_database()
        except Exception as e:
            logging.error(f"Error during table creation or data import: {e}")

        # Start bot polling
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
