from aiogram.types import Message, ContentTypes, ReplyKeyboardRemove
from keyboards.default.key import main_menu, menu, phone_num
from loader import dp, bot, db
import sqlite3
from data.config import ADMINS
from states.personalData import PersonalData
from aiogram.dispatcher import FSMContext

@dp.message_handler(commands='start')
async def start(msg: Message):
    user = db.select_user(id=msg.from_user.id)
    if not user:
        await msg.answer(f"Assalomu alaykum {msg.from_user.get_mention()}\n\n"
                         f"Botimizga xush kelibsiz, botdan foydalanish uchun ro'yxatdan o'ting!", reply_markup=main_menu)
    else:
        await msg.answer("Kerakli bo'limni tanlang", reply_markup=menu)

@dp.message_handler(text="Ro'yxatdan o'tish")
async def roy(message: Message):
    await message.answer("\n\n"
                         "Misol uchun: Asqarov Alisher", reply_markup=ReplyKeyboardRemove())
    await PersonalData.fullName.set()

@dp.message_handler(state=PersonalData.fullName)
async def reg_ism(message: Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer("📲 Telefon raqamni yuboring\n"
                         "Yoki shunchaki yozing", reply_markup=phone_num)
    await PersonalData.phoneNumber.set()

@dp.message_handler(state=PersonalData.phoneNumber, content_types=ContentTypes.ANY)
async def reg_phone(message: Message, state: FSMContext):
    async with state.proxy() as data:
        ism = data.get('ism')
    if message.contact:
        await message.answer("Kerakli bo'limni tanlang", reply_markup=menu)
        db.add_user(id=message.from_user.id, fullname=ism, phone=message.contact.phone_number)
        for ADMIN in ADMINS:
            await bot.send_message(chat_id=ADMIN, text=f"Ism: {ism}\n\n"
                                                       f"Telefon: {message.contact.phone_number}\n\n"
                                                       f"Ro'yxatdan o'tdi!")
            son = db.count_users()[0]
            await bot.send_message(chat_id=ADMIN, text=f"Botdagi foydalanuvchilar: {son} ta")
            await state.finish()
    else:
        try:
            int(message.text)
            text = message.text
            result = text.startswith('+998')
            if result == True:
                await message.answer("Kerakli bo'limni tanlang", reply_markup=menu)
                db.add_user(id=message.from_user.id, fullname=ism, phone=message.text)
                for adminn in ADMINS:
                    await bot.send_message(chat_id=adminn, text=f"Ism : {ism}\n\n"
                                                               f"Telefon: {message.text}\n\n"
                                                               f"Ro'yxatdan o'tdi !")
                son = db.count_users()[0]
                for admin in ADMINS:
                    await bot.send_message(chat_id=admin, text=f"Botdagi foydulanuvchilar soni {son} dona !")
                    await state.finish()
            else:
                await message.answer("❌ Iltimos O'zbekiston telefon raqamini kiriting\n\n"
                                     "Misol uchun: +998991234567")
        except:
            await message.answer("❌ Telefon raqamni sonlarda kiriting\n\n"
                                 "Misol uchun: +998991234567")