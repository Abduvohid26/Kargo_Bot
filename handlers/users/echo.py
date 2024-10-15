from loader import dp
from aiogram import types,F
from filters.admin_filter import Member
from aiogram import html

@dp.message(F.text, Member())
async def echo_bot(message:types.Message):
    text = (f"Sizga qanday yordam kerak\n"
            f"Admin Bilan Aloqa {html.link(value='Abdugani', link='tg://user?id=147737693')}\n"
            f"/start   /help")
    await message.answer(text=text)