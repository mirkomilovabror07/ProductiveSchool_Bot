from aiogram.dispatcher.filters.state import State, StatesGroup

class starter(StatesGroup):
    starter_num = State()

class beginner(StatesGroup):
    beginner_num = State()

class elementary(StatesGroup):
    elementary_num = State()

class pre_intermediate(StatesGroup):
    pre_intermediate_num = State()

class intermediate(StatesGroup):
    intermediate_num = State()

class upper_intermediate(StatesGroup):
    upper_intermediate_num = State()