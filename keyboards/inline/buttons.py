from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from loader import db

class CheckCall(CallbackData, prefix="ikb"):
    check: bool


def check_button():
    btn = InlineKeyboardBuilder()
    btn.button(text='✅ Ha', callback_data=CheckCall(check=True))
    btn.button(text='❌ Yoq', callback_data=CheckCall(check=False))
    btn.adjust(2)
    return btn.as_markup()


def signup():
    btn = InlineKeyboardBuilder()
    btn.button(text="📑 Royxatdan o'tish", callback_data="register")
    btn.adjust(1)
    return btn.as_markup()


def update_options(sj, js):
    btn = InlineKeyboardBuilder()
    btn.button(text="📌 Ism va Familya", callback_data="update_name")
    btn.button(text=js, callback_data="update_phone")
    btn.button(text="📝 Qoshimcha Ma'lumotni", callback_data="update_additional_info")
    btn.button(text="🖼 Manzilni", callback_data="update_address")
    btn.button(text=sj, callback_data="update_kargo")
    btn.adjust(2)
    return btn.as_markup()

def get_unique_region_names():
    region_data = db.select_all_address()
    unique_region_names = list(set(region[-1] for region in region_data))
    return unique_region_names[:15]

def region_button():
    region_names = get_unique_region_names()
    btn = InlineKeyboardBuilder()
    for region_name in region_names:
        btn.button(text=region_name, callback_data=f'region_{region_name.lower()}')
    btn.adjust(2)
    return btn.as_markup()


class CheckAuto(CallbackData, prefix="ikb26"):
    check: bool


def check_add_auto():
    btn = InlineKeyboardBuilder()
    btn.button(text='✅ Ha', callback_data=CheckAuto(check=True))
    btn.button(text='❌ Yoq', callback_data=CheckAuto(check=False))
    btn.adjust(2)
    return btn.as_markup()

def check_admin():
    btn = InlineKeyboardBuilder()
    btn.button(text="✅ Admin tekshirish", callback_data="check_admin")
    return btn.as_markup()


def admin_delete():
    btn = InlineKeyboardBuilder()
    btn.button(text="❌ Admin O'chirish", callback_data="delete_admin")
    return btn.as_markup()


class CheckAdminDelete(CallbackData, prefix='ikb2629'):
    check: bool

def check_admin_delete():
    btn = InlineKeyboardBuilder()
    btn.button(text='✅ Ha', callback_data=CheckAdminDelete(check=True))
    btn.button(text='❌ Yoq', callback_data=CheckAdminDelete(check=False))
    btn.adjust(2)
    return btn.as_markup()

def admin_add_button():
    btn = InlineKeyboardBuilder()
    btn.button(text="Admin Qo'shish ➕", callback_data="add_admin")
    btn.adjust(1)
    return btn.as_markup()

# class CheckAdminAdd(CallbackData, prefix='ikb22'):
#     check: bool
#
# def check_admin_add_button():
#     btn = InlineKeyboardBuilder()
#     btn.button(text='✅ Ha', callback_data=CheckAdminAdd(check=True))
#     btn.button(text='❌ Yoq', callback_data=CheckAdminAdd(check=False))
#     btn.adjust(2)
#     return btn.as_markup()


class CheckOrder(CallbackData, prefix='ikb12'):
    check: bool

def check_order_button():
    btn = InlineKeyboardBuilder()
    btn.button(text='✅ Ha', callback_data=CheckOrder(check=True))
    btn.button(text='❌ Yoq', callback_data=CheckOrder(check=False))
    btn.adjust(2)
    return btn.as_markup()




class CheckOrderPay(CallbackData, prefix='ikb11'):
    check: bool

def check_order_pay_button():
    btn = InlineKeyboardBuilder()
    btn.button(text='✅ Tolangan', callback_data=CheckOrderPay(check=True))
    btn.button(text='❌ Tolanmagan', callback_data=CheckOrderPay(check=False))
    btn.adjust(2)
    return btn.as_markup()

class CheckOrderChangePay(CallbackData, prefix='ikb91'):
    check: bool

def check_order_pay_change_button():
    btn = InlineKeyboardBuilder()
    btn.button(text='✅ Tolangan', callback_data=CheckOrderChangePay(check=True))
    btn.button(text='❌ Tolanmagan', callback_data=CheckOrderChangePay(check=False))
    btn.adjust(2)
    return btn.as_markup()


def check_admin_add_button():
    btn = InlineKeyboardBuilder()
    btn.button(text="✅ Ha", callback_data="ha")
    btn.button(text="❌ Yo'q", callback_data="yoq")
    btn.adjust(2)
    return btn.as_markup()

def prog():
    btn = InlineKeyboardBuilder()
    btn.button(text="✅ Programmalarga to'g'ri kiritish uchun na'munalar", callback_data="prog")
    btn.adjust(2)
    return btn.as_markup()
