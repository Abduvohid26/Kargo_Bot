from loader import bot, db, dp
from aiogram import F, types
from keyboards.default.buttons import update_button


@dp.message(F.text == '📄 Ma\'lumotlarim')
async def get_client_data(message: types.Message):
    data = db.select_user(telegram_id=message.from_user.id)
    user_id = data[-4]
    name = data[1]
    phone = data[4]
    phone_number = data[5]
    manzil = data[6]
    tuman = data[-8]
    exact_address = data[-6]
    saja = data[-10] if data[-10] else None
    sj_avia = data[-9] if data[-9] else None
    description = data[-5]
    text = f"📑 Siznig  ma'lumotlaringiz\n"
    text += f"📌 Ism Familya: {name}\n"
    text += f"☎️ Telefon Raqam: {phone}\n"
    if phone_number is not None:
        text += f"☎️ Qo'shimcha Telefon Raqam: {phone_number}\n"
    text += f"🖼 Viloyat: {manzil}\n"
    text += f"🏙 Tuman: {tuman}\n"
    text += f"🚪 Aniq Manzil: {exact_address}\n"
    if saja:
        text += f"🚚 Cleint Auto ID: {saja}\n"
    if sj_avia:
        text += f"✈️ Cleint Avia ID: {sj_avia}\n"
    text += f"📝 Qoshimcha Ma'lumot: {description}"
    await message.answer(text, reply_markup=update_button())