from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from loader import db

user_level_callback = CallbackData("level_call", "level")
user_mashq_callback = CallbackData("mashq_call", "level", "mashq")
user_edit_kabinet_callback = CallbackData("edit_cabinet_call", 'holat')

edit_cabinet = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 Ism o'zgartirish", callback_data=user_edit_kabinet_callback.new(holat='ism'))
        ],
        [
            InlineKeyboardButton(text="📞 Telefon raqamni o'zgartirish", callback_data=user_edit_kabinet_callback.new(holat='telefon'))
        ]
    ]
)

user_levelkey = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Starter", callback_data=user_level_callback.new(level='starter'))
        ],
        [
            InlineKeyboardButton(text='Beginner', callback_data=user_level_callback.new(level='beginner'))
        ],
        [
            InlineKeyboardButton(text='Elementary', callback_data=user_level_callback.new(level='elementary'))
        ],
        [
            InlineKeyboardButton(text="Pre-Intermediate", callback_data=user_level_callback.new(level='pre_intermediate'))
        ],
        [
            InlineKeyboardButton(text="Intermediate", callback_data=user_level_callback.new(level='intermediate'))
        ],
        [
            InlineKeyboardButton(text="Upper-Intermediate", callback_data=user_level_callback.new(level='upper_intermediate'))
        ]
    ]
)

def user_mashqkey(level):
    mashqlar = db.select_all_keyboard(types=level)
    key = InlineKeyboardMarkup(row_width=3)
    for mashq in mashqlar:
        key.insert(InlineKeyboardButton(text=mashq[2], callback_data=user_mashq_callback.new(level=level, mashq=mashq[2])))
    key.add(InlineKeyboardButton(text="◀️ Orqaga", callback_data=user_mashq_callback.new(level=level, mashq='orqaga')))
    return key