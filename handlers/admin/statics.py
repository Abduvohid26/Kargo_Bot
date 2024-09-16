from loader import bot, db, dp
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from states.my_state import OrderFilterStatus
from keyboards.inline.buttons import check_order_pay_change_button, CheckOrderChangePay
from keyboards.default.buttons import year_button, month_buttons, status_buttons
import pandas as pd
from openpyxl import Workbook
from io import BytesIO
from datetime import datetime
import os
from openpyxl.drawing.image import Image  # Rasmlarni qo'shish uchun import


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

    if status == "Barchasi":
        orders = db.select_orders_by_date(year, month)
        file_status = "barchasi"
    else:
        is_paid = (status == "To'langan")
        orders = db.select_orders_by_date_and_status(year=year, month=month, status=is_paid)
        file_status = "tolangan" if is_paid else "tolanmagan"

    wb = Workbook()
    ws = wb.active
    ws.title = "Buyurtmalar"

    # Sarlavhalarni qo'shish
    headers = ["Buyurtma ID", "Client ID", "Buyurtmalar soni", "Kg", "Hajm", "Reys raqami", "Narx", "Status",
               "Buyurtma rasmi", "Yaratilgan vaqt", "O'zgartirilgan vaqt", "Admin Yaratilgan vaqt", "Admin qilingan vaqt"]
    ws.append(headers)

    for idx, order in enumerate(orders, start=2):
        client_id = order[1]
        client_suffix = client_id[-3:]
        cur_user = db.select_user_by_saja_value(f"SAJA-{client_suffix}")
        cur_user1 = db.select_user_by_sj_avia_value(f"SJ-avia-{client_suffix}")
        if cur_user:
            created_admin_id = cur_user[-2]
            updated_admin_id = cur_user[-1]
        elif cur_user1:
            created_admin_id = cur_user1[-2]
            updated_admin_id = cur_user1[-1]
        else:
            created_admin_id = "Noma'lum"
            updated_admin_id = "Noma'lum"

        row_data = list(order) + [
            "",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            created_admin_id,
            updated_admin_id
        ]
        ws.append(row_data)
        image_path = order[8]
        if os.path.exists(image_path):
            img = Image(image_path)
            img.width = 40
            img.height = 40
            ws.add_image(img, f"H{idx}")
        else:
            ws[f"H{idx}"] = "Rasm mavjud emas"

    file_name = f'{year}-{month}-{file_status}.xlsx'
    file_path = file_name
    wb.save(file_path)

    try:
        await message.answer_document(
            document=types.input_file.FSInputFile(file_path, filename=file_name),
            caption="Filtrlash natijalari"
        )
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)