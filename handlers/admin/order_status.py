from loader import bot, db, dp
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from states.my_state import OrderChangeStatus
from keyboards.inline.buttons import check_order_pay_change_button, CheckOrderChangePay


@dp.message(F.text == "📬 Buyurtma Statusini o'zgartirish 🔄")
async def get_id(message: types.Message, state: FSMContext):
    await message.answer("📬 Buyurtma ID sini kiriting yoki 👤 Client ID kiriting:")
    await state.set_state(OrderChangeStatus.start)


@dp.message(F.text, OrderChangeStatus.start)
async def start_change(message: types.Message, state: FSMContext):
    input_data = message.text
    if input_data.isdigit():
        data = db.select_order(order_id=input_data)
    else:
        data = db.select_order(client_id=input_data)

    if data:
        await message.answer(f"Buyurtma ma'lumotlari:\n"
                             f"Buyurtma ID: {data[-1]}\n"
                             f"Client ID: {data[1]}\n"
                             f"Buyurtmalar soni: {data[4]}\n"
                             f"Kg: {data[2]}\n"
                             f"Hajm: {data[3]}\n"
                             f"Reys raqami: {data[6]}\n"
                             f"Narx: {data[5]}\n"
                             f"""Status: {"🟩 To'langan" if data[7] else "🟧 To'lanmagan"}""")
        await state.update_data({"id": data[-1]})
        await message.answer("📬 Buyurtma statusini tanlang:", reply_markup=check_order_pay_change_button())
        await state.set_state(OrderChangeStatus.final)
    else:
        await message.answer("❌ Buyurtma topilmadi. Iltimos, qayta urinib ko'ring.")


@dp.callback_query(CheckOrderChangePay.filter(), OrderChangeStatus.final)
async def final(call: types.CallbackQuery, callback_data: CheckOrderChangePay, state: FSMContext):
    check = callback_data.check
    data = await state.get_data()
    order_id = data['id']

    if check:
        db.update_order_field(order_id=order_id, field="status", value=True)
    else:
        db.update_order_field(order_id=order_id, field="status", value=False)

    updated_data = db.select_order(order_id=order_id)

    await call.message.answer(f"Buyurtma holati muvaffaqiyatli yangilandi:\n"
                              f"Buyurtma ID: {updated_data[-1]}\n"
                              f"Client ID: {updated_data[1]}\n"
                              f"Buyurtmalar soni: {updated_data[4]}\n"
                              f"Kg: {updated_data[2]}\n"
                              f"Hajm: {updated_data[3]}\n"
                              f"Reys raqami: {updated_data[6]}\n"
                              f"Narx: {updated_data[5]}\n"
                              f"""Status: {"🟩 To'langan" if updated_data[7] else "🟧 To'lanmagan"}""")

    await state.clear()
    await call.message.delete()
