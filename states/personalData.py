from aiogram.dispatcher.filters.state import State, StatesGroup

class PersonalData(StatesGroup):
    fullName = State()
    phoneNumber = State()

class edit_cabinet_state(StatesGroup):
    ism = State()
    phone = State()