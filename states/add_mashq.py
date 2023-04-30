from aiogram.dispatcher.filters.state import State, StatesGroup

class add_mashq_state(StatesGroup):
    mashq = State()

class add_savol_state(StatesGroup):
    savol = State()
    javob = State()
    izoh = State()

class edit_savol_state(StatesGroup):
    savol = State()
    javob = State()
    izoh = State()