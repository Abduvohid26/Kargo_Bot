from aiogram import types
from loader import bot, db
from aiogram.filters import Filter

class Admin(Filter):
    async def __call__(self, message: types.Message) -> bool:
        user = db.select_user(is_staff=True, telegram_id=message.from_user.id)
        if user:
            return True
        return False

class Member(Filter):
    async def __call__(self, message: types.Message) -> bool:
        user = db.select_user(is_staff=False, telegram_id=message.from_user.id)
        if user:
            return True
        return False


class AdminMember(Filter):
    async def __call__(self, message: types.Message) -> bool:
        user = db.select_user(is_staff=True, telegram_id=message.from_user.id)
        if user:
            return False
        return True
