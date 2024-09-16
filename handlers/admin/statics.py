from loader import bot, db, dp
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from states.my_state import OrderFilterStatus
from keyboards.inline.buttons import check_order_pay_change_button, CheckOrderChangePay
from keyboards.default.buttons import year_button, month_buttons, status_buttons
import pandas as pd
from openpyxl import Workbook
from io import BytesIO
import os

@dp.message(F.text == "📊 Statistika")
async def choose_year(message: types.Message, state: FSMContext):
    await message.answer("Yilni tanlang:", reply_markup=year_button())
    await state.set_state(OrderFilterStatus.year)


@dp.message(F.text, OrderFilterStatus.year)
async def choose_month(message: types.Message, state: FSMContext):
    year = message.text
    await state.update_data(year=year)
    await message.answer("Oyni tanlang:", reply_markup=month_buttons())
    await state.set_state(OrderFilterStatus.month)

@dp.message(F.text, OrderFilterStatus.month)
async def choose_status(message: types.Message, state: FSMContext):
    month = message.text
    await state.update_data(month=month)
    await message.answer("Buyurtma statusini tanlang:", reply_markup=status_buttons())
    await state.set_state(OrderFilterStatus.status)


@dp.message(F.text, OrderFilterStatus.status)
async def generate_report(message: types.Message, state: FSMContext):
    status = message.text
    data = await state.get_data()
    year = data.get("year")
    month = data.get("month")
    print(month, year, data)

    if status == "Barchasi":
        orders = db.select_orders_by_date(year, month)
        print(orders, 'd')
    else:
        is_paid = (status == "To'langan")
        orders = db.select_orders_by_date_and_status(year=year, month=month, status=is_paid)
        print(orders, 's')

    wb = Workbook()
    ws = wb.active
    ws.title = "Buyurtmalar"

    headers = ["Buyurtma ID", "Client ID", "Buyurtmalar soni", "Kg", "Hajm", "Reys raqami", "Narx", "Status"]
    ws.append(headers)

    for order in orders:
        ws.append(order)

    file_path = "buyurtmalar.xlsx"
    wb.save(file_path)

    try:
        await message.answer_document(
            document=types.input_file.FSInputFile(file_path, filename="buyurtmalar.xlsx"),
            caption="Filtrlash natijalari"
        )
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)