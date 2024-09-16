from aiogram.fsm.state import State, StatesGroup

class Register(StatesGroup):
    name = State()
    phone = State()
    phone_number = State()
    address = State()
    Kargo = State()
    check = State()
    district = State()
    exact_address = State()
    description = State()

class UpdateState(StatesGroup):
    choose_field = State()
    name = State()
    phone = State()
    address = State()
    district = State()
    kargo = State()
    exact_address = State()
    description = State()

class AdminCheckState(StatesGroup):
    start = State()
    final = State()


class AdminDelete(StatesGroup):
    start = State()
    final = State()

# class AdminAdd(StatesGroup):
#     start = State()
#     final = State()
#     check = State()


class AddOrderState(StatesGroup):
    image = State()
    qty = State()
    client_id = State()
    kg = State()
    hajm = State()
    price = State()
    reiz_number = State()
    status = State()
    check = State()


class OrderChangeStatus(StatesGroup):
    start = State()
    final = State()


class OrderFilterStatus(StatesGroup):
    start = State()  # Buyurtma ID yoki Client ID ni olish uchun holat
    year = State()   # Yilni tanlash uchun holat
    month = State()  # Oyni tanlash uchun holat
    status = State() # Buyurtma statusini tanlash uchun



# Admin qo'shish jarayoni uchun State lar
class AdminAdd(StatesGroup):
    enter_phone = State()  # Telefon raqamini kiritish
    confirm = State()      # Admin qilishni tasdiqlash
    final = State()        # Yangi adminni tasdiqlash
    check = State()        # Ha/Yo'q tugmasi bosilgandan keyin holat
