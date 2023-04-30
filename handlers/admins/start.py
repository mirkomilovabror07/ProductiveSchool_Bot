from aiogram.types import Message
from loader import db, dp
from data.config import ADMINS
from keyboards.inline.admin_keyboard import admin_Panel, admin_ortacha_Panel

@dp.message_handler(commands='admin', chat_id=ADMINS)
async def admin_start(message: Message):
    await message.answer("👮🏻‍♂️ Admin panelga xush kelibsiz!", reply_markup=admin_Panel)

@dp.message_handler(commands='admin')
async def adminlar(message: Message):
    user = db.select_admin(id=message.from_user.id)
    if user:
        await message.answer("👮🏻‍♂️ Admin panelga xush kelibsiz !", reply_markup=admin_ortacha_Panel)

@dp.message_handler(commands='cleandb', chat_id=ADMINS)
async def cleandb(message: Message):
    db.delete_users()
    await message.answer("Bazadagi foydalanuvchilar o'chirildi")

@dp.message_handler(commands='cleanex', chat_id=ADMINS)
async def cleandb(message: Message):
    db.delete_mashq()
    await message.answer("Bazadagi mashqlar o'chirildi")

@dp.message_handler(commands='cleanbtns', chat_id=ADMINS)
async def cleandb(message: Message):
    db.delete_keayboards()
    await message.answer("Bazadagi tugmalar o'chirildi")