from aiogram.utils.keyboard import ReplyKeyboardBuilder

def start_button():
    btn = ReplyKeyboardBuilder()
    btn.button(text="Ro'yxatdan o'tish")
    btn.adjust(1)
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)


def kargo_type():
    btn = ReplyKeyboardBuilder()
    btn.button(text='🚚 Auto')
    btn.button(text='✈️ Avia')
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)


def client_button():
    btn = ReplyKeyboardBuilder()
    btn.button(text='📄 Ma\'lumotlarim')
    btn.button(text='☎️ Aloqa')
    btn.button(text='📬 Buyurtmalarim')
    btn.button(text='➕ Buyurtma berish')
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_phone_number_button():
    btn = ReplyKeyboardBuilder()
    btn.button(text="📞 Telefon raqamni yuborish", request_contact=True)
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)


def update_button():
    btn = ReplyKeyboardBuilder()
    btn.button(text="🔄 Ma'lumotlarni Yangilash")
    btn.button(text="◀️ Ortga")
    btn.adjust(1)
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)

def skip_button():
    btn = ReplyKeyboardBuilder()
    btn.button(text="◀️ O'tkazib Yuborish")
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)


def admin_button():
    btn = ReplyKeyboardBuilder()
    btn.button(text="⚙️ Admin")
    btn.button(text="📊 Statistika")
    btn.button(text="📬 Buyurtma Qo\'shish")
    btn.button(text="📬 Buyurtma Statusini o'zgartirish 🔄")
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)


def admin_include():
    btn = ReplyKeyboardBuilder()
    btn.button(text="⚙️ Admin Qoshish ➕")
    btn.button(text="⚙️ Admin List")
    btn.button(text="👤 Users List")
    btn.button(text="◀️ Orqaga")
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)


def year_button():
    btn = ReplyKeyboardBuilder()
    btn.button(text="2024")
    btn.button(text="2025")
    btn.button(text="◀️ Orqaga")
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)

def month_buttons():
    btn = ReplyKeyboardBuilder()
    btn.button(text="Yanvar")
    btn.button(text="Fevral")
    btn.button(text="Mart")
    btn.button(text="Aprel")
    btn.button(text="May")
    btn.button(text="Iyun")
    btn.button(text="Iyul")
    btn.button(text="Avgust")
    btn.button(text="Sentabr")
    btn.button(text="Oktyabr")
    btn.button(text="Noyabr")
    btn.button(text="Dekabr")
    btn.button(text="◀️ Orqaga")
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)


def status_buttons():
    btn = ReplyKeyboardBuilder()
    btn.button(text="To'langan")
    btn.button(text="To'lanmagan")
    btn.button(text="Barchasi")
    btn.button(text="◀️ Orqaga")
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)

