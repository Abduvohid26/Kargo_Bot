from aiogram.filters import CommandStart
from loader import dp, db
from aiogram import types, F
from keyboards.default.buttons import start_button, kargo_type, client_button, get_phone_number_button, skip_button
from aiogram.fsm.context import FSMContext
from states.my_state import Register
from keyboards.inline.buttons import check_button, CheckCall, signup, region_button
import uuid
import random
import asyncio
from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.message(CommandStart())
async def start_bot(message: types.Message):
    if db.select_user(telegram_id=message.from_user.id):
        await message.answer(f"Assalamu Aleykum {message.from_user.full_name}", reply_markup=client_button())
    else:
        await message.answer(f"Assalomu alaykum {message.from_user.full_name}!"
                             f" Botimizga xush kelibsiz", reply_markup=signup())


@dp.callback_query(lambda query: query.data.startswith('register'))
async def get_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Ism va Familyangizni kiriting:")
    await call.answer(cache_time=60)
    await state.set_state(Register.name)


@dp.message(F.text, Register.name)
async def get_phone(msg: types.Message, state: FSMContext):
    name = msg.text
    await state.update_data({"name": name})
    await msg.answer(f"Telefon raqamingizni yuboring:", reply_markup=get_phone_number_button())
    await state.set_state(Register.phone)


@dp.message(F.contact, Register.phone)
async def get_contact(message: types.Message, state: FSMContext):
    if message.contact and message.contact.phone_number:
        phone = message.contact.phone_number
        await state.update_data({"phone": phone})
        await message.answer(f"Qo'shimcha telefon raqamingizni kiriting: Masalan: +9981234567",
                             reply_markup=skip_button())
        await state.set_state(Register.phone_number)
    else:
        await message.answer("Telefon raqamini ulashishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")


@dp.message(F.text, Register.phone_number)
async def get_address(msg: types.Message, state: FSMContext):
    phone_number = msg.text
    if phone_number == "◀️ O'tkazib Yuborish":
        phone_number = None
    await state.update_data({"phone_number": phone_number})
    await msg.answer("Viloyatni tanlang", reply_markup=region_button())
    await state.set_state(Register.address)


@dp.callback_query(lambda query: query.data.startswith('region_'), Register.address)
async def get_districts(call: types.CallbackQuery, state: FSMContext):
    region_name = call.data.split('_')[-1].capitalize()
    data = db.select_address(region_name=region_name)

    if not data:
        await call.answer("Region topilmadi.")
        return

    region_id = data[2]
    datas = db.select_district_names_by_region_id(region_id=region_id)
    btn = InlineKeyboardBuilder()

    for district in datas:
        btn.button(text=district, callback_data=f"district_{district}")

    btn.adjust(2)
    await state.update_data({"region": region_name})
    await call.message.edit_text("Tumanlarni tanlang:", reply_markup=btn.as_markup())
    await state.set_state(Register.district)

@dp.callback_query(lambda query: query.data.startswith('district_'), Register.district)
async def get_exact_address(call: types.CallbackQuery, state: FSMContext):
    district_name = call.data.split('_')[-1]
    await state.update_data({"district": district_name})
    await call.answer(cache_time=60)
    await call.message.answer(f"Tumanni tanladingiz: {district_name}: Endi aniq manzil kiriting:"
                              f"Masalan {district_name} Alisher N kochasi 17 uy")
    await state.set_state(Register.exact_address)

@dp.message(F.text, Register.exact_address)
async def get_kargo(message: types.Message, state: FSMContext):
    exact_address = message.text
    await state.update_data(
        {
            "exact_address": exact_address
        }
    )
    await message.answer(f"Endi kargo turini tanlang:", reply_markup=kargo_type())
    await state.set_state(Register.Kargo)


@dp.message(F.text.in_(['🚚 Auto', '✈️ Avia']), Register.Kargo)
async def get_description(msg: types.Message, state: FSMContext):
    kargo = msg.text
    await state.update_data({"kargo": kargo})
    await msg.answer(F"Qoshimcha malumot kiriting:")
    await state.set_state(Register.description)


@dp.message(F.text, Register.description)
async def final(msg: types.Message, state: FSMContext):
    description = msg.text
    await state.update_data({"description": description})
    data = await state.get_data()

    phone_number = data.get('phone_number')

    text = f"📑 Ushbu ma'lumotlar to'g'rimi?\n"
    text += f"📌 Ism Familya: {data.get('name', 'N/A')}\n"
    text += f"☎️ Telefon Raqam: {data.get('phone', 'N/A')}\n"
    if phone_number:
        text += f"☎️ Qo'shimcha Telefon Raqam: {phone_number}\n"
    text += f"🖼 Viloyat: {data.get('region', 'N/A')}\n"
    text += f"🏙 Tuman: {data.get('district', 'N/A')}\n"
    text += f"🚪 Aniq Manzil: {data.get('exact_address', 'N/A')}\n"
    text += f"📦 Kargo turi: {data.get('kargo', 'N/A')}\n"
    text += f"📝 Qoshimcha Ma'lumot: {data.get('description', 'N/A')}"
    await msg.answer(text=text, reply_markup=check_button())
    await state.set_state(Register.check)


@dp.callback_query(CheckCall.filter(), Register.check)
async def check_data(call: types.CallbackQuery, callback_data: CheckCall, state: FSMContext):
    check = callback_data.check
    await call.answer(cache_time=60)
    while True:
        user_ids = random.randint(100000, 999999)
        s = random.randint(100, 999)
        saja_value = f'SAJA-{s}'
        sj_avia_value = f'SJ-avia-{s}'
        existing_saja = db.select_user_by_saja_value(saja_value)
        existing_sj_avia = db.select_user_by_sj_avia_value(sj_avia_value)
        if not existing_saja and not existing_sj_avia:
            break

    if check:
        data = await state.get_data()
        user_id = str(uuid.uuid4())
        fullname = data['name']
        telegram_id = call.from_user.id
        language = call.from_user.language_code
        phone = data['phone']
        phone_number = data['phone_number']
        manzil = data['region']
        tuman = data['district']
        kargo = data['kargo']
        exact_address = data['exact_address']
        description = data['description']
        saja = saja_value if kargo == '🚚 Auto' else None
        sj_avia = sj_avia_value if kargo == '✈️ Avia' else None

        db.add_user(
            id=user_id,
            fullname=fullname,
            telegram_id=telegram_id,
            language=language,
            phone=phone,
            phone_number=phone_number,
            manzil=manzil,
            tuman=tuman,
            saja=saja,
            sj_avia=sj_avia,
            exact_address=exact_address,
            description=description,
            user_id=user_ids
        )
        await call.message.answer("Muvaffaqiyatli ro'yxatdan o'tdingiz 👏", reply_markup=client_button())
    else:
        await call.message.answer("Qaytadan ro'yxatdan o'ting\n"
                                  "/start")
        await call.message.delete()

    await asyncio.sleep(5)
    await state.clear()


@dp.message(F.text == '📬 Buyurtmalarim')
async def user_orders(message: types.Message):
    user_data = db.select_user(telegram_id=message.from_user.id)
    print(user_data)
    if not user_data:
        await message.answer("Foydalanuvchi topilmadi.")
        return

    saja_id = user_data[7]
    saja_id1 = user_data[6]
    if saja_id1:
        orders = db.select_orders_by_saja_id(saja_id=f'SAJA-{saja_id[-3:]}')
    elif saja_id:
        orders = db.select_orders_by_saja_id(saja_id=f'SJ-avia-{saja_id1[-3:]}')




    if orders:
        order_list = []
        for order in orders:
            order_list.append(
                f"Buyurtma ID: {order[0]}\n"
                f"Buyurtma miqdori: {order[2]}\n"
                f"Narxi: {order[5]}\n"
                f"Status: {'To\'langan' if order[6] == 1 else 'To\'lanmagan'}\n\n"
            )
        await message.answer("Buyurtmalaringiz:\n\n" + "".join(order_list))
    else:
        await message.answer("Sizda hech qanday buyurtma mavjud emas.")