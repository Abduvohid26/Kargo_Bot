from aiogram import Bot,Dispatcher
from data.config import BOT_TOKEN
# Import Database Class
from utils.db_api.sqlite import Database
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
import pytz
from datetime import datetime
bot=Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp=Dispatcher(storage=MemoryStorage())
# Create database file
db = Database(path_to_db='data/main.db')
# Tashkent vaqt zonasini olish
tashkent_tz = pytz.timezone('Asia/Tashkent')

# Hozirgi vaqtni Tashkent vaqt zonasida olish
tashkent_time = datetime.now(tashkent_tz)

created_at = datetime.now(tashkent_tz)
updated_at = datetime.now(tashkent_tz)