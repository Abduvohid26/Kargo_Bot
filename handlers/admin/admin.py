import os.path
from loader import db, dp, tashkent_time
from aiogram.filters import Command
from aiogram import types, F
from filters.admin_filter import Admin
from keyboards.default.buttons import admin_button, admin_include
from keyboards.inline.buttons import check_admin, admin_delete, check_admin_delete, CheckAdminDelete, check_admin_add_button, admin_add_button
import pandas as pd
from states.my_state import AdminCheckState, AdminDelete, AdminAdd
from aiogram.fsm.context import FSMContext
@dp.message(Command('admin'), Admin())
async def admin_bot(message: types.Message):
    await message.answer("🔝 Admin Panel", reply_markup=admin_button())


@dp.message(F.text == '⚙️ Admin')
async def get_admin_include(message: types.Message):
    await message.answer("Admin Parametlari ⚙️", reply_markup=admin_include())


@dp.message(F.text == '👤 Users List')
async def users_list(message: types.Message):
    data = db.get_users_by_activation_status(is_staff=False)

    if not data:
        await message.answer(f"Hozirda userlar ma'lumoti mavjud emas !!!")
        return

    users_data = []

    for user in data:
        user_info = {
            "Ism Familyasi": user[1],
            "Phone": user[4],
            "Manzil": user[6],
            "Tuman": user[9],
            "Aniq Manzil": user[11],
            "Qoshimcha Ma'lumot": user[12],
            "User ID": user[13],
            "Qo'shilgan vaqt": user[-2],
        }

        user_info["Phone Number"] = user[5] if user[5] else None

        user_info["SAJA"] = user[7] if user[7] else None
        user_info["SAJA Avia"] = user[8] if user[8] else None

        users_data.append(user_info)

    df = pd.DataFrame(users_data)

    file_path = "users_list.xlsx"
    df.to_excel(file_path, index=False)

    excel_file = types.input_file.FSInputFile(file_path)

    await message.answer_document(excel_file, caption="Foydalanuvchilar ma'lumotlari Excel faylda")
    if os.path.isfile(file_path):
        os.remove(file_path)


@dp.message(F.text == '⚙️ Admin List')
async def get_admin_list(message: types.Message, state: FSMContext):
    datas = db.get_users_by_activation_status(is_staff=True)
    if not datas:
        await message.answer("Hozirda userlar ma'lumoti mavjud emas !!!")
        return

    admin_list = ""
    for data in datas:
        full_name = data[1]
        if data[7]:
            id = f"SAJA-{data[7][-3:]}"
        else:
            id = f"SAJA-{data[8][-3:]}"

        admin_list += (f"Ism Familyasi: {full_name}\n"
                       f"ID: {id}\n\n")

    text = f"👤 Adminlar Ro'yxati:\n\n{admin_list}"
    await message.answer(text=text, reply_markup=check_admin())
    await state.set_state(AdminCheckState.start)


@dp.callback_query(lambda query: query.data == 'check_admin', AdminCheckState.start)
async def ask_admin_id(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Admin ID sini kiriting:")
    await state.set_state(AdminCheckState.final)
    await call.answer()

@dp.message(F.text, AdminCheckState.final)
async def verify_admin(message: types.Message, state: FSMContext):
    user_data = message.text[-3:]
    user_exists = db.select_user(saja=f"SAJA-{user_data}")
    user_data_exists = db.select_user(sj_avia=f"SJ-avia-{user_data}")

    if user_exists or user_data_exists:
        user_info = user_exists if user_exists else user_data_exists
        telegram_id = user_info[2]
        fish = user_info[1]
        phone_number = user_info[4] if user_info[4] else "Telefon raqam kiritilmagan"
        region = user_info[6] if user_info[6] else "Viloyat kiritilmagan"
        district = user_info[9] if user_info[9] else "Tuman kiritilmagan"
        exact_address = user_info[11] if user_info[11] else "Manzil kiritilmagan"
        qoshimcha_malumot = user_info[12] if user_info[12] else "Qoshimcha Malumot Kiritilmagan"
        saja_id = f'SAJA-{user_info[7][-3:]}' if user_info[7] else f'SAJA-{user_info[8][-3:]}'
        add_user = user_info[14] if user_info[14] else "Developer tomonidan yaratilgan"
        cur_user = db.select_user(telegram_id=add_user)
        if cur_user:
            cur_fish = cur_user[1] if cur_user[1] else "Ism Familyasi mavjud emas"
            cur_phone_number = cur_user[4] if cur_user[4] else "Telefon raqam kiritilmagan"
            cur_region = cur_user[6] if cur_user[6] else "Viloyat kiritilmagan"
            cur_district = cur_user[9] if cur_user[9] else "Tuman kiritilmagan"
            cur_exact_address = cur_user[11] if cur_user[11] else "Manzil kiritilmagan"
            cur_saja_id = f'SAJA-{cur_user[7][-3:]}' if cur_user[7] else f'SAJA-{cur_user[8][-3:]}'
            qoshimcha_malumot_cure = cur_user[12] if cur_user[12] else "Qoshimcha Malumot Kiritilmagan"
        else:
            cur_fish = cur_phone_number = cur_region = cur_district = cur_exact_address = cur_saja_id = "Ma'lumot mavjud emas"
        await message.answer(
            text=f"Ism Familyasi: {fish}\n"
                 f"ID: {saja_id}\n"
                 f"Telefon raqami: {phone_number}\n"
                 f"Viloyat: {region}\n"
                 f"Tuman: {district}\n"
                 f"Aniq manzil: {exact_address}\n"
                 f"Qo'shimcha ma'lumot: {qoshimcha_malumot}\n\n" 
                 f"Quyidagi admin tomonidan qo'shilgan:\n"
                 f"Ism Familyasi: {cur_fish}\n"
                 f"ID: {cur_saja_id}\n"
                 f"Telefon raqami: {cur_phone_number}\n"
                 f"Viloyat: {cur_region}\n"
                 f"Tuman: {cur_district}\n"
                 f"Aniq manzil: {cur_exact_address}"
                f"Qo'shimcha ma'lumot: {qoshimcha_malumot_cure}",

        reply_markup=admin_delete()
    )
        await state.update_data({
            "telegram_id": telegram_id,
            "saja": saja_id,
            "fish": fish,
            "phone_number": phone_number,
            "region": region,
            "district": district,
            "exact_address": exact_address
        })
        await state.set_state(AdminDelete.start)

    else:
        await message.answer(f"Ushbu ID: {message.text} bo'yicha ma'lumot topilmadi!!!")
        await state.set_state(AdminDelete.start)

@dp.callback_query(lambda query: query.data == 'delete_admin', AdminDelete.start)
async def admin_deletes(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("O'chirishni tasdiqlang:", reply_markup=check_admin_delete())
    await call.answer()
    await state.set_state(AdminDelete.final)


@dp.callback_query(CheckAdminDelete.filter(), AdminDelete.final)
async def admin_final_delete(call: types.CallbackQuery, callback_data: CheckAdminDelete, state: FSMContext):
    check = callback_data.check
    data = await state.get_data()
    telegram_id = data['telegram_id']
    saja = data['saja']
    fish = data['fish']

    # O'chirilayotgan foydalanuvchining ma'lumotlarini olish
    user_data_exists = db.select_user(telegram_id=telegram_id)
    admin_data_exists = db.select_user(telegram_id=call.from_user.id)

    user_id = f'SAJA-{user_data_exists[7][-3:]}' if user_data_exists[7] else f'SAJA-{user_data_exists[8][-3:]}'
    user_full_name = user_data_exists[1]
    user_address = f'{user_data_exists[6]}, {user_data_exists[9]}'  # Foydalanuvchi manzili
    user_phone = user_data_exists[4]  # Foydalanuvchi telefon raqami
    user_extra_info = user_data_exists[9]  # Foydalanuvchi qo'shimcha ma'lumot
    delete_time = tashkent_time.strftime("%Y-%m-%d %H:%M:%S")  # Operatsiya vaqti

    # O'chiruvchi adminning ma'lumotlari
    admin_id = f'SAJA-{admin_data_exists[7][-3:]}' if admin_data_exists[7] else f'SAJA-{admin_data_exists[8][-3:]}'
    admin_full_name = admin_data_exists[1]  # Admin ism familyasi
    admin_address = f'{admin_data_exists[6]}, {admin_data_exists[9]}'  # Admin manzili
    admin_phone = admin_data_exists[4]  # Admin telefon raqami
    admin_extra_info = admin_data_exists[9]  # Admin qo'shimcha ma'lumot
    await call.answer(cache_time=60)

    if check:
        # Foydalanuvchini adminlikdan chiqarish
        db.update_user_field(telegram_id=telegram_id, field="is_staff", value=0)
        db.update_user_field(telegram_id=telegram_id, field="updated_at", value=tashkent_time)

        await call.message.answer(
            text=f"❌ Admin muvaffaqiyatli o'chirildi:\n\n"
                 f"📋 **O'chirilgan foydalanuvchi ma'lumotlari:**\n"
                 f"ID: {user_id}\n"
                 f"Ism Familya: {user_full_name}\n"
                 f"Manzil: {user_address}\n"
                 f"Telefon raqami: {user_phone}\n"
                 f"Qo'shimcha ma'lumot: {user_extra_info}\n\n"
                 f"🔧 **Operatsiyani amalga oshirgan admin ma'lumotlari:**\n"
                 f"Admin ID: {admin_id}\n"
                 f"Ism Familya: {admin_full_name}\n"
                 f"Manzil: {admin_address}\n"
                 f"Telefon raqami: {admin_phone}\n"
                 f"Qo'shimcha ma'lumot: {admin_extra_info}\n"
                 f"Operatsiya vaqti: {delete_time}"
        )
    else:
        await call.message.answer("❌ O'chirish bekor qilindi")

    await state.clear()

#
# @dp.message(F.text == "⚙️ Admin Qoshish ➕")
# async def users_lists(message: types.Message, state: FSMContext):
#     user_data = db.get_users_by_activation_status(is_staff=False)
#     user_list = []
#     for user in user_data:
#         user_id = f'SAJA-{user[7][-3:]}' if user[7] else f'SAJA-{user[8][-3:]}'
#         fullname = user[1]
#         phone = user[4] if user[4] else "Telefon raqam yo'q"  # phone
#         address = user[6] if user[6] else "Manzil yo'q"  # address
#         tuman = user[9] if user[9] else "Tuman yo'q"  # district
#
#         user_list.append(f"ID: {user_id}\nIsm: {fullname}\nTelefon: {phone}\nManzil: {address} viloyati, {tuman} tumani\n\n")
#     await message.answer("Userlar ro'yxati 📝")
#     await message.answer("".join(user_list) if user_list else "Hech qanday foydalanuvchi topilmadi.", reply_markup=admin_add_button())
#     await state.set_state(AdminAdd.start)
#
#
#
# @dp.callback_query(lambda query: query.data == 'add_admin', AdminAdd.start)
# async def do_admin(call: types.CallbackQuery, state: FSMContext):
#     await call.message.answer("Yangi Admin ID sini kiriting:")
#     await state.set_state(AdminAdd.final)



# @dp.message(F.text == "⚙️ Admin Qoshish ➕")
# async def users_lists(message: types.Message, state: FSMContext):
#     user_data = db.get_users_by_activation_status(is_staff=False)
#     user_list = []
#     for user in user_data:
#         user_id = f'SAJA-{user[7][-3:]}' if user[7] else f'SAJA-{user[8][-3:]}'
#         fullname = user[1]
#         phone = user[4] if user[4] else "Telefon raqam yo'q"  # phone
#         address = user[6] if user[6] else "Manzil yo'q"  # address
#         tuman = user[9] if user[9] else "Tuman yo'q"  # district
#
#         user_list.append(
#             f"ID: {user_id}\nIsm: {fullname}\nTelefon: {phone}\nManzil: {address} viloyati, {tuman} tumani\n\n")
#
#     await message.answer("Userlar ro'yxati 📝")
#     await message.answer("".join(user_list) if user_list else "Hech qanday foydalanuvchi topilmadi.",
#                          reply_markup=admin_add_button())
#     await state.set_state(AdminAdd.start)
#
#
# @dp.callback_query(lambda query: query.data == 'add_admin', AdminAdd.start)
# async def do_admin(call: types.CallbackQuery, state: FSMContext):
#     await call.message.answer("Yangi Admin ID sini kiriting:")
#     await call.answer(cache_time=60)
#     await state.set_state(AdminAdd.final)
#
#
# @dp.message(F.text, AdminAdd.final)
# async def final_admin(message: types.Message, state: FSMContext):
#     new_admin = message.text.strip()
#     await state.update_data({"new_admin": new_admin})
#     await message.answer(f"Siz kiritgan admin ID: {new_admin}. Tasdiqlaysizmi?", reply_markup=check_admin_add_button())
#     await state.set_state(AdminAdd.check)
#
#
# logger = logging.getLogger(__name__)
#
# @dp.callback_query(CheckAdminAdd.filter(), AdminAdd.check)
# async def check_admin_add(call: types.CallbackQuery, callback_data: CheckAdminAdd, state: FSMContext):
#     data = await state.get_data()
#     check = callback_data.check
#     new_admin_id = data.get("new_admin", "")
#
#     if len(new_admin_id) < 3:
#         await call.message.answer("ID juda qisqa. Iltimos, to'g'ri ID kiriting.")
#         return
#
#     new_admin_id = new_admin_id[-3:]
#     user_id = f'SAJA-{new_admin_id}'
#     user_avia_id = f'SJ-avia-{new_admin_id}'
#
#     logger.info(f"Checking user ID: {user_id}, Avia ID: {user_avia_id}")
#
#     user_exists = db.select_user(saja=user_id)
#     user_dats_avia = db.select_user(sj_avia=user_avia_id)
#     fish = user_exists[1] if user_exists else (user_dats_avia[1] if user_dats_avia else "Ism topilmadi")
#
#     current_user = db.select_user(telegram_id=call.from_user.id)
#     current_user_id = current_user[7] if current_user and current_user[7] else (current_user[8] if current_user and current_user[8] else "ID topilmadi")
#
#     if (user_exists or user_dats_avia) and check:
#         telegram_id = user_exists[2] if user_exists else (user_dats_avia[2] if user_dats_avia else None)
#         if telegram_id:
#             db.update_user_field(telegram_id=telegram_id, field="is_staff", value=1)
#             db.update_user_field(telegram_id=telegram_id, field="updated_at", value=tashkent_time)
#             await call.message.answer(
#                 f"Admin muvaffaqiyatli qo'shildi:\n"
#                 f"Ism: {fish}\n"
#                 f"ID: SAJA-{new_admin_id}\n\n"
#                 f"Quyidagi admin tomonidan qo'shildi:\n"
#                 f"Ism: {current_user[1] if current_user else 'N/A'}\n"
#                 f"ID: SAJA-{current_user_id[-3:] if current_user_id != 'ID topilmadi' else 'N/A'}"
#                  f"Operatsiya Vaqti: {tashkent_time}"
#             )
#         else:
#             await call.message.answer("Telegram ID topilmadi.")
#     else:
#         await call.message.answer(f"ID: {new_admin_id} bo'yicha foydalanuvchi topilmadi yoki tasdiqlanmagan.")
#
#     await state.clear()
#
# @dp.message(F.text == '◀️ Orqaga')
# async def get_back(message: types.Message):
#     await message.answer(text="🔝 Admin Panel", reply_markup=admin_button())

@dp.message(F.text == "⚙️ Admin Qoshish ➕")
async def request_phone_number(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, yangi adminning telefon raqamini kiriting:")
    await state.set_state(AdminAdd.enter_phone)


@dp.message(F.text, AdminAdd.enter_phone)
async def check_user_by_phone(message: types.Message, state: FSMContext):
    phone_number = message.text.strip()

    user = db.get_user_by_phone(phone=phone_number)

    if user:
        user_id = f'SAJA-{user[7][-3:]}' if user[7] else f'SAJA-{user[8][-3:]}'
        fullname = user[1]
        address = user[6] if user[6] else "Manzil yo'q"
        tuman = user[9] if user[9] else "Tuman yo'q"
        telegram_id = user[2]

        await state.update_data({"user_id": user_id, "fullname": fullname, "phone": phone_number, "telegram_id": telegram_id})
        await message.answer(
            f"Topilgan foydalanuvchi:\n"
            f"ID: {user_id}\nIsm: {fullname}\nTelefon: {phone_number}\nManzil: {address}, {tuman}\n\n"
            f"Ushbu foydalanuvchini admin qilishni tasdiqlaysizmi?",
            reply_markup=check_admin_add_button()
        )
        await state.set_state(AdminAdd.confirm)
    else:
        await message.answer("Foydalanuvchi topilmadi. Iltimos, telefon raqamini tekshiring.")
        await state.clear()


@dp.callback_query(lambda query: query.data in ["ha", "yoq"], AdminAdd.confirm)
async def confirm_admin_add(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    response = call.data
    data = await state.get_data()
    user_id = data.get("user_id")
    fullname = data.get("fullname")
    phone_number = data.get("phone")
    telegram_id = data.get("telegram_id")
    current_user = db.select_user(telegram_id=call.from_user.id)
    current_user_id = current_user[7] if current_user and current_user[7] else (current_user[8] if current_user and current_user[8] else "ID topilmadi")
    if response == "ha":
        db.update_user_field(telegram_id=telegram_id, field="is_staff", value=1)
        db.update_user_field(telegram_id=telegram_id, field="updated_at", value=tashkent_time)
        db.update_user_field(telegram_id=telegram_id, field="add_user", value=call.from_user.id)

        await call.message.answer(
            f"Admin muvaffaqiyatli qo'shildi:\n"
            f"Ism: {fullname}\nID: {user_id}\nTelefon: {phone_number}\n"
            f"Quyidagi admin tomonidan qo'shildi:\n"
            f"Ism: {current_user[1] if current_user else 'N/A'}\n"
            f"ID: SAJA-{current_user_id[-3:] if current_user_id != 'ID topilmadi' else 'N/A'}"
            f"Operatsiya vaqti: {tashkent_time}\n"

        )
    else:
        await call.message.answer("Admin qo'shish jarayoni bekor qilindi.")

    await state.clear()


@dp.message(F.text == '◀️ Orqaga')
async def get_back(message: types.Message):
    await message.answer(text="🔝 Admin Panel", reply_markup=admin_button())
