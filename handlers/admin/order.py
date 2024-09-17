from keyboards.default.buttons import admin_button
from loader import bot, db, dp, tashkent_time, created_at, updated_at
from aiogram import types, F
from states.my_state import AddOrderState
from aiogram.fsm.context import FSMContext
from keyboards.inline.buttons import CheckOrderPay, check_order_pay_button, check_order_button, CheckOrder
from filters.admin_filter import Admin
import asyncio
import os
import random
SAVE_DIRECTORY = 'media'
@dp.message(F.text == '📬 Buyurtma Qo\'shish', Admin())
async def add_order_page(message: types.Message, state: FSMContext):
    await message.answer(text='📬 Buyurtma rasmini kiriting:')
    await state.set_state(AddOrderState.image)


@dp.message(F.photo, AddOrderState.image, Admin())
async def get_qty(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file = await bot.get_file(file_id=photo.file_id)
    saved_path = os.path.join(SAVE_DIRECTORY, f"{photo.file_id}.jpg")
    await bot.download(file, destination=saved_path)
    image_url = f"{saved_path}"

    await state.update_data({'image_url': image_url})

    await message.answer(text="📬 Buyurtma sonini kiriting:")
    await state.set_state(AddOrderState.qty)


@dp.message(F.text, AddOrderState.qty, Admin())
async def get_client_id(message: types.Message, state: FSMContext):
    qty = message.text
    await state.update_data({'qty': qty})
    await message.answer(text="📬 Buyurtma egasini kiriting (client_id):")
    await state.set_state(AddOrderState.client_id)


@dp.message(F.text, AddOrderState.client_id, Admin())
async def get_price(message: types.Message, state: FSMContext):
    client_id = message.text
    await state.update_data({'client_id': client_id})
    await message.answer(text="📬 Buyurtma narxini kiriting (price):")
    await state.set_state(AddOrderState.price)


@dp.message(F.text, AddOrderState.price, Admin())
async def get_kg(message: types.Message, state: FSMContext):
    price = message.text
    await state.update_data({'price': price})
    await message.answer(text="📬 Buyurtma kg kiriting:")
    await state.set_state(AddOrderState.kg)


@dp.message(F.text, AddOrderState.kg, Admin())
async def get_hajm(message: types.Message, state: FSMContext):
    kg = message.text
    await state.update_data({'kg': kg})
    await message.answer(text="📬 Buyurtma hajmini kiriting:")
    await state.set_state(AddOrderState.hajm)


@dp.message(F.text, AddOrderState.hajm, Admin())
async def get_reiz_number(message: types.Message, state: FSMContext):
    hajm = message.text
    await state.update_data({'hajm': hajm})
    await message.answer(text="📬 Buyurtma reis raqamini kiriting:")
    await state.set_state(AddOrderState.reiz_number)


@dp.message(F.text, AddOrderState.reiz_number, Admin())
async def get_status(message: types.Message, state: FSMContext):
    reiz_number = message.text
    await state.update_data({'reiz_number': reiz_number})
    await message.answer(text="📬 Buyurtma statusini tanlang:", reply_markup=check_order_pay_button())
    await state.set_state(AddOrderState.status)


@dp.callback_query(CheckOrderPay.filter(), AddOrderState.status, Admin())
async def enter_check(call: types.CallbackQuery, callback_data: CheckOrderPay, state: FSMContext):
    check = callback_data.check
    value = 0
    if check:
        value = 1
    await state.update_data({'value': value})
    await call.answer(cache_time=60)
    data = await state.get_data()
    text = f"📑 Ushbu ma'lumotlar to'g'rimi?\n"
    text += f"Client ID: {data['client_id']}\n"
    text += f"Buyurtmalar soni: {data['qty']}\n"
    text += f"Buyurtma Kg: {data['kg']}\n"
    text += f"Buyurtma Hajmi: {data['hajm']}\n"
    text += f"Buyurtma reys raqami: {data['reiz_number']}\n"
    text += f"Buyurtma narxi: {data['price']}\n"

    if data['value'] == 1:
        text += f"\nBuyurtma To'langan 🟩"
    else:
        text += f"\nBuyurtma To'lanmagan 🟧"

    await call.message.answer(text=text, reply_markup=check_order_button())
    await state.set_state(AddOrderState.check)


@dp.callback_query(CheckOrder.filter(), AddOrderState.check, Admin())
async def final(call: types.CallbackQuery, callback_data: CheckOrder, state: FSMContext):
    check = callback_data.check
    await call.answer(cache_time=60)
    user_ids = random.randint(100000, 999999)
    if check:
        data = await state.get_data()
        client_id = data.get("client_id")
        qty = data.get("qty")
        kg = data.get("kg")
        hajm = data.get("hajm")
        reiz_number = data.get("reiz_number")
        price = data.get("price")
        status = data.get("value") == 1
        image = data.get("image_url")

        db.add_order(client_id=client_id, qty=qty, kg=kg, hajm=hajm, price=price, reiz_number=reiz_number,
                     status=status, created_at=created_at, updated_at=updated_at,
                     image=image, order_id=user_ids)

        await call.message.answer(f"Buyurtma muvaffaqiyatli qo'shildi:\n"
                                  f"Buyurtma ID: {user_ids}\n"
                                  f"Client ID: {client_id}\n"
                                  f"Buyurtmalar soni: {qty}\n"
                                  f"Kg: {kg}\n"
                                  f"Hajm: {hajm}\n"
                                  f"Reys raqami: {reiz_number}\n"
                                  f"Narx: {price}\n"
                                  f"""Status: {"🟩 To'langan" if status else "🟧 To'lanmagan"}""")

        await state.clear()
        return

    await call.message.answer("Buyurtmani qayta qoshing", reply_markup=admin_button())
    await state.clear()
    await asyncio.sleep(5)
    await call.message.delete()



