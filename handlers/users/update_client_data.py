from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram import F
from loader import dp, db
from keyboards.inline.buttons import update_options, region_button ,CheckAuto, check_add_auto
from keyboards.default.buttons import client_button
from states.my_state import UpdateState
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random
from filters.admin_filter import Admin, Member

@dp.message(F.text == "🔄 Ma'lumotlarni Yangilash", Member())
async def update_info(message: types.Message, state: FSMContext):
    user_data = db.select_user(telegram_id=message.from_user.id)
    js = ""
    text = ""
    if user_data[-10] and user_data[-9]:
        text += ""
    elif user_data[-9]:
        text +=  "🚚 Auto Qo'shish"
    else:
        text += "✈️ Avia Qo'shish"
    if user_data[5]:
        js += "☎️ Qoshimcha Telefon Raqam"
    else:
        js += ""
    await message.answer(
        "📄 Qaysi ma'lumotni yangilamoqchisiz tanlang?",
        reply_markup=update_options(sj=text, js=js)
    )
    await state.set_state(UpdateState.choose_field)

@dp.message(F.text == '◀️ Ortga', Member())
async def get_back(message: types.Message, state: FSMContext):
    await message.answer("🎛 Asosiy Menu", reply_markup=client_button())
    await state.clear()

@dp.callback_query(F.data == "update_name", UpdateState.choose_field)
async def update_name(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer("Yangi ismingizni kiriting:")
    await state.set_state(UpdateState.name)


@dp.callback_query(F.data == "update_phone", UpdateState.choose_field)
async def update_phone(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer("Yangi telefon raqamingizni kiriting:")
    await state.set_state(UpdateState.phone)


@dp.callback_query(F.data == "update_address", UpdateState.choose_field)
async def update_address(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer("Yangi viloyatingizni tanlang:", reply_markup=region_button())
    await state.set_state(UpdateState.address)


@dp.callback_query(F.data == "update_kargo", UpdateState.choose_field)
async def update_kargo(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer("Haqiqattan ham qo'shishni xoxlaysizmi ?", reply_markup=check_add_auto())
    await state.set_state(UpdateState.kargo)

@dp.callback_query(F.data == "update_additional_info", UpdateState.choose_field)
async def update_additional_info(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer("Qo'shimcha ma'lumot kiriting:")
    await state.set_state(UpdateState.description)


@dp.message(F.text, UpdateState.description)
async def exact_address(message: types.Message, state: FSMContext):
    new_name = message.text
    db.update_user_field(telegram_id=message.from_user.id, field="description", value=new_name)
    await message.answer("Qoshimcha Malumot muvaffaqiyatli yangilandi!", reply_markup=client_button())
    await state.clear()


@dp.message(F.text, UpdateState.name)
async def save_name(message: types.Message, state: FSMContext):
    new_name = message.text
    db.update_user_field(telegram_id=message.from_user.id, field="fullname", value=new_name)
    await message.answer("Ismingiz muvaffaqiyatli yangilandi!", reply_markup=client_button())
    await state.clear()


@dp.message(F.text, UpdateState.phone)
async def save_phone(message: types.Message, state: FSMContext):
    new_phone = message.text
    db.update_user_field(telegram_id=message.from_user.id, field="phone_number", value=new_phone)
    await message.answer("Telefon raqamingiz muvaffaqiyatli yangilandi!", reply_markup=client_button())
    await state.clear()



@dp.callback_query(lambda query: query.data.startswith('region_'), UpdateState.address)
async def select_district(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    region_name = call.data.split('_')[-1].capitalize()
    await state.update_data({"region": region_name})
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
    await call.message.edit_text("Yangi tumanni tanlang:", reply_markup=btn.as_markup())
    await state.set_state(UpdateState.district)
    await call.answer(cache_time=60)


@dp.callback_query(lambda query: query.data.startswith('district_'), UpdateState.district)
async def get_choose_exact_address(call: types.CallbackQuery, state: FSMContext):
    district_name = call.data.split('_')[-1]
    await state.update_data({
        "district_name": district_name
    })
    await call.answer(cache_time=60)
    await call.message.answer("Yangi Aniq manzilni kiriting:")
    await state.set_state(UpdateState.exact_address)


@dp.message(F.text, UpdateState.exact_address)
async def save_address(message: types.Message, state: FSMContext):
    exact_address = message.text
    data = await state.get_data()

    db.update_user_field(
        telegram_id=message.from_user.id,
        field="manzil",
        value=data['region']
    )
    db.update_user_field(
        telegram_id=message.from_user.id,
        field="tuman",
        value=data["district_name"]
    )
    db.update_user_field(
        telegram_id=message.from_user.id,
        field="exact_address",
        value=exact_address
    )

    await message.answer("Manzilingiz muvaffaqiyatli yangilandi!", reply_markup=client_button())
    await state.clear()


@dp.callback_query(CheckAuto.filter(), UpdateState.kargo)
async def save_kargo(call: types.CallbackQuery, state: FSMContext, callback_data: CheckAuto):
    await call.answer(cache_time=60)
    check = callback_data.check
    if check:
        user = db.select_user(telegram_id=call.from_user.id)
        while True:
            s = random.randint(100, 999)
            saja_value = f"SAJA-{s}"
            sj_avia_value = f"SJ-avia-{s}"

            existing_saja = db.select_user_by_saja_value(saja_value)
            existing_sj_avia = db.select_user_by_sj_avia_value(sj_avia_value)

            if not existing_saja and not existing_sj_avia:
                break

        if user and user[-1]:
            db.update_user_field(telegram_id=call.from_user.id, field="saja", value=saja_value)

        db.update_user_field(telegram_id=call.from_user.id, field="sj_avia", value=sj_avia_value)
        await call.message.answer("Yangi tur muvaffaqiyatli qo'shildi!", reply_markup=client_button())
    else:
        await call.message.answer("Qo'shish bekor qilindi", reply_markup=client_button())
    await state.clear()
