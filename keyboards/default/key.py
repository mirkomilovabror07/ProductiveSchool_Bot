from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ro'yxatdan o'tish"),
        ],
    ],
    resize_keyboard=True
)

phone_num = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📲 Telefon raqamni yuborish", request_contact=True),
        ],
    ],
    resize_keyboard=True
)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Mashq bajarish"),
            KeyboardButton(text="👤 Shaxsiy kabinet")
        ],
    ],
    resize_keyboard=True
)

backButton_ex = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="◀️ Ortga")
        ],
    ],
    resize_keyboard=True
)