from loader import bot, db, dp, tashkent_time
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from states.my_state import OrderChangeStatus
from keyboards.inline.buttons import check_order_pay_change_button, CheckOrderChangePay
from data.config import SEO
from filters.admin_filter import Admin

@dp.message(F.text == "📬 Buyurtma Statusini o'zgartirish 🔄", Admin())
async def get_id(message: types.Message, state: FSMContext):
    await message.answer("📬 Buyurtma ID sini kiriting yoki 👤 Client ID kiriting:")
    await state.set_state(OrderChangeStatus.start)


@dp.message(F.text, OrderChangeStatus.start, Admin())
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


@dp.callback_query(CheckOrderChangePay.filter(), OrderChangeStatus.final, Admin())
async def final(call: types.CallbackQuery, callback_data: CheckOrderChangePay, state: FSMContext):
    check = callback_data.check
    data = await state.get_data()
    order_id = data['id']

    # O'zgartirgan foydalanuvchining ma'lumotlarini olish
    admin_data_exists = db.select_user(telegram_id=call.from_user.id)

    if admin_data_exists:
        admin_id = f'SAJA-{admin_data_exists[7][-3:]}' if admin_data_exists[7] else f'SAJA-{admin_data_exists[8][-3:]}'
        admin_full_name = admin_data_exists[1]
        admin_address = f'{admin_data_exists[6] or "N/A"}, {admin_data_exists[9] or "N/A"}'
        admin_phone = admin_data_exists[4] or 'N/A'
        admin_extra_info = admin_data_exists[9] or 'N/A'
    else:
        admin_id = 'N/A'
        admin_full_name = 'N/A'
        admin_address = 'N/A'
        admin_phone = 'N/A'
        admin_extra_info = 'N/A'

    if check:
        db.update_order_field(order_id=order_id, field="status", value=True)
    else:
        db.update_order_field(order_id=order_id, field="status", value=False)

    updated_data = db.select_order(order_id=order_id)
    change_time = tashkent_time.strftime("%Y-%m-%d %H:%M:%S")

    await call.message.answer(f"Buyurtma holati muvaffaqiyatli yangilandi:\n"
                              f"📋 **Buyurtma ma'lumotlari:**\n"
                              f"Buyurtma ID: {updated_data[-1]}\n"
                              f"Client ID: {updated_data[1]}\n"
                              f"Buyurtmalar soni: {updated_data[4]}\n"
                              f"Kg: {updated_data[2]}\n"
                              f"Hajm: {updated_data[3]}\n"
                              f"Reys raqami: {updated_data[6]}\n"
                              f"Narx: {updated_data[5]}\n"
                              f"""Status: {"🟩 To'langan" if updated_data[7] else "🟧 To'lanmagan"}"""
                              f"🔧 **O'zgartirishni amalga oshirgan admin ma'lumotlari:**\n"
                              f"Admin ID: {admin_id}\n"
                              f"Ism Familya: {admin_full_name}\n"
                              f"Manzil: {admin_address}\n"
                              f"Telefon raqami: {admin_phone}\n"
                              f"Qo'shimcha ma'lumot: {admin_extra_info}\n"
                              f"Operatsiya vaqti: {change_time}"
                              )
    await bot.send_message(chat_id=SEO,
                           text=f"Buyurtma holati muvaffaqiyatli yangilandi:\n"
                              f"📋 **Buyurtma ma'lumotlari:**\n"
                              f"Buyurtma ID: {updated_data[-1]}\n"
                              f"Client ID: {updated_data[1]}\n"
                              f"Buyurtmalar soni: {updated_data[4]}\n"
                              f"Kg: {updated_data[2]}\n"
                              f"Hajm: {updated_data[3]}\n"
                              f"Reys raqami: {updated_data[6]}\n"
                              f"Narx: {updated_data[5]}\n"
                              f"""Status: {"🟩 To'langan" if updated_data[7] else "🟧 To'lanmagan"}"""
                              f"🔧 **O'zgartirishni amalga oshirgan admin ma'lumotlari:**\n"
                              f"Admin ID: {admin_id}\n"
                              f"Ism Familya: {admin_full_name}\n"
                              f"Manzil: {admin_address}\n"
                              f"Telefon raqami: {admin_phone}\n"
                              f"Qo'shimcha ma'lumot: {admin_extra_info}\n"
                              f"Operatsiya vaqti: {change_time}")


    await state.clear()
    await call.message.delete()