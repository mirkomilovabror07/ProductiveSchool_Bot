from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from loader import db, bot

admin_menu_callback = CallbackData("admin_menu", "holat")
add_level_callback = CallbackData("add_level", 'level')
add_mashq_callback = CallbackData("add_mashq", "level", "mashq")
add_savol_callback = CallbackData("add_savol", "level", "mashq", "id")
savol_edit_callback = CallbackData("savol_edit_call", "level", "mashq", "id", "holat")
adminlar_callback = CallbackData("adminlar", "id")

admin_Panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📣 Reklama yuborish', callback_data=admin_menu_callback.new(holat='reklama')),
            InlineKeyboardButton(text='📊 Bot Statistikasi', callback_data=admin_menu_callback.new(holat='statik')),
        ],
        [
            InlineKeyboardButton(text="➕ Mashq qo'shish ➕", callback_data=admin_menu_callback.new(holat='mashq'))
        ],
        [
            InlineKeyboardButton(text="👮 Adminlar", callback_data=admin_menu_callback.new(holat='admin')),
            InlineKeyboardButton(text="👥 Userlar ro'yxati", callback_data=admin_menu_callback.new(holat='user'))
        ]
    ],
)

admin_ortacha_Panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📣 Reklama yuborish', callback_data=admin_menu_callback.new(holat='reklama')),
            InlineKeyboardButton(text='📊 Bot Statistikasi', callback_data=admin_menu_callback.new(holat='statik')),
        ],
        [
            InlineKeyboardButton(text="➕ Mashq qo'shish ➕", callback_data=admin_menu_callback.new(holat='mashq'))
        ],
        [
            InlineKeyboardButton(text="👥 Userlar ro'yxati", callback_data=admin_menu_callback.new(holat='user'))
        ]
    ],
)

add_for_level = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Starter", callback_data=add_level_callback.new(level='starter'))
        ],
        [
            InlineKeyboardButton(text="Beginner", callback_data=add_level_callback.new(level='beginner'))
        ],
        [
            InlineKeyboardButton(text="Elementary", callback_data=add_level_callback.new(level='beginner'))
        ],
        [
            InlineKeyboardButton(text="Pre-Intermediate", callback_data=add_level_callback.new(level='pre_intermediate'))
        ],
        [
            InlineKeyboardButton(text="Intermediate", callback_data=add_level_callback.new(level='intermediate'))
        ],
        [
            InlineKeyboardButton(text="Upper-Intermediate", callback_data=add_level_callback.new(level='upper_intermediate'))
        ],
        [
            InlineKeyboardButton(text="◀️ Orqaga", callback_data=add_level_callback.new(level='orqaga'))
        ]
    ]
)

def add_mashqkey(level):
    key = InlineKeyboardMarkup(row_width=3)
    keys = db.select_all_keyboard(types=level)
    for k in keys:
        key.insert(InlineKeyboardButton(text=k[2], callback_data=add_mashq_callback.new(level=level, mashq=k[2])))
    key.add(InlineKeyboardButton(text="➕ Mashq qo'shish ➕", callback_data=add_mashq_callback.new(level=level, mashq='add_mashq')),
            InlineKeyboardButton(text="◀️ Orqaga", callback_data=add_mashq_callback.new(level=level, mashq='orqaga')))
    return key

def add_savol(level, mashq):
    savollar = db.select_all_mashq(daraja=level, mashq=mashq)
    key = InlineKeyboardMarkup()
    son = 1
    for savol in savollar:
        key.add(InlineKeyboardButton(text=f"{son} - savol", callback_data=add_savol_callback.new(level=level, mashq=mashq, id=savol[0])))
        son += 1
    key.add(InlineKeyboardButton(text="➕ Savol qo'shish ➕", callback_data=add_savol_callback.new(level=level, mashq=mashq, id='add_savol')),
            InlineKeyboardButton(text="◀️ Orqaga", callback_data=add_savol_callback.new(level=level, mashq=mashq, id='orqaga')))
    return key

izoh_yoqkey = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Izoh yo'q", callback_data='yoq')
        ]
    ]
)

def savol_edit_key(level, mashq, id):
    key = InlineKeyboardMarkup(row_width=1)
    key.insert(InlineKeyboardButton(text="📝 Savolni tahrirlash", callback_data=savol_edit_callback.new(level=level, mashq=mashq, id=id, holat='savol')))
    key.insert(InlineKeyboardButton(text="📝 Javobni tahrirlash", callback_data=savol_edit_callback.new(level=level, mashq=mashq, id=id, holat='javob')))
    key.insert(InlineKeyboardButton(text="📝 Izohni tahrirlash", callback_data=savol_edit_callback.new(level=level, mashq=mashq, id=id, holat='izoh')))
    key.insert(InlineKeyboardButton(text="◀️ Orqaga", callback_data=savol_edit_callback.new(level=level, mashq=mashq, id=id, holat='orqaga')))
    return key

async def adminlar_key():
    admins = db.select_all_admin()
    key = InlineKeyboardMarkup(row_width=1)
    for admin in admins:
        user = await bot.get_chat(chat_id=admin[0])
        key.insert(InlineKeyboardButton(text=f"{user.full_name}", callback_data=adminlar_callback.new(id=admin[0])))
    key.add(InlineKeyboardButton(text="➕ Admin qo'shish", callback_data=adminlar_callback.new(id='add')))
    key.insert(InlineKeyboardButton(text="◀️ Orqaga",callback_data=adminlar_callback.new(id='orqaga')))
    return key