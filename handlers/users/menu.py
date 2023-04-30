from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentTypes
from loader import dp, db, bot
from keyboards.inline.user_keyboard import user_levelkey, user_level_callback, user_mashq_callback, user_mashqkey, user_edit_kabinet_callback, edit_cabinet
from keyboards.default.key import menu, phone_num
from states.mashq_bajarish_state import mashqbajarish_state
from states.personalData import edit_cabinet_state
from aiogram.dispatcher import FSMContext
from data.config import ADMINS

@dp.message_handler(text="Mashq bajarish")
async def mahq_bajarish_hand(message: Message):
    await message.answer("Kerakli darajani tanlang 👇", reply_markup=user_levelkey)

@dp.callback_query_handler(user_level_callback.filter())
async def user_level_hand(call: CallbackQuery, callback_data: dict):
    level = callback_data.get('level')
    key = user_mashqkey(level=level)
    await call.message.edit_text(f"{level} darajaning kerakli mashqni tanlang 👇", reply_markup=key)

@dp.callback_query_handler(user_mashq_callback.filter())
async def user_mashq_hand(call: CallbackQuery, state: FSMContext, callback_data: dict):
    level = callback_data.get('level')
    mashq = callback_data.get('mashq')
    if mashq == 'orqaga':
        key = user_mashqkey(level=level)
        await call.message.answer("Kerakli darajani tanlang 👇", reply_markup=user_levelkey)
    else:
        await mashqbajarish_state.mashq.set()
        await call.message.delete()
        mashqlar = db.select_all_mashq(daraja=level, mashq=mashq)
        await call.message.answer("🖋 Savollarga javob yozing\n"
                                  "Bekor qilish uchun /stop buyrug'ini bosing", reply_markup=ReplyKeyboardRemove())
        await state.update_data(level=level)
        await state.update_data(mashq=mashq)
        await state.update_data(son=1)
        await call.message.answer(mashqlar[0][3])

@dp.message_handler(state=mashqbajarish_state.mashq, commands='stop')
async def stop_mashq(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Mashq to'xtatildi!")
    await message.answer("Kerakli darajani tanlang 👇", reply_markup=user_levelkey)

@dp.message_handler(state=mashqbajarish_state.mashq)
async def mashq_state_hand(message: Message, state: FSMContext):
    async with state.proxy() as data:
        level = data.get('level')
        mashq = data.get('mashq')
        son = int(data.get('son'))
        javob1 = data.get('javob1')
        javob2 = data.get('javob2')
        javob3 = data.get('javob3')
        javob4 = data.get('javob4')
        javob5 = data.get('javob5')
    mashqlar = db.select_all_mashq(daraja=level, mashq=mashq)
    if len(mashqlar) == son:
        x = 1
        result = ""
        if javob1:
            for javob in javob1.split('/'):
                izoh = mashqlar[x-1][5]
                if izoh == 'yoq':
                    result += f"{x}.{mashqlar[x-1][3]}\n♻️ {javob}\n✅ {mashqlar[x-1][4]}\n\n"
                else:
                    result += f"{x}.{mashqlar[x-1][3]}\n♻️ {javob}\n✅ {mashqlar[x-1][4]}\n💡 <tg-spoiler>{izoh}</tg-spoiler>\n\n"
                x += 1
        if javob2:
            for javob in javob2.split('/'):
                izoh = mashqlar[x-1][5]
                if izoh == 'yoq':
                    result += f"{x}.{mashqlar[x - 1][3]}\n♻️ {javob}\n✅ {mashqlar[x - 1][4]}\n\n"
                else:
                    result += f"{x}.{mashqlar[x - 1][3]}\n♻️ {javob}\n✅ {mashqlar[x - 1][4]}\n💡 <tg-spoiler>{izoh}</tg-spoiler>\n\n"
                x+=1
        if javob3:
            for javob in javob3.split('/'):
                izoh = mashqlar[x-1][5]
                if izoh == 'yoq':
                    result += f"{x}.{mashqlar[x-1][3]}\n♻️ {javob}\n✅ {mashqlar[x-1][4]}\n\n"
                else:
                    result += f"{x}.{mashqlar[x-1][3]}\n♻️ {javob}\n✅ {mashqlar[x-1][4]}\n💡 <tg-spoiler>{izoh}</tg-spoiler>\n\n"
                x+=1
        if javob4:
            for javob in javob4.split('/'):
                izoh = mashqlar[x-1][5]
                if izoh == 'yoq':
                    result += f"{x}.{mashqlar[x-1][3]}\n♻️ {javob}\n✅ {mashqlar[x-1][4]}\n\n"
                else:
                    result += f"{x}.{mashqlar[x-1][3]}\n♻️ {javob}\n✅ {mashqlar[x-1][4]}\n💡 <tg-spoiler>{izoh}</tg-spoiler>\n\n"
                x+=1
        if javob5:
            for javob in javob5.split('/'):
                izoh = mashqlar[x-1][5]
                if izoh == 'yoq':
                    result += f"{x}.{mashqlar[x-1][3]}\n♻️ {javob}\n✅ {mashqlar[x-1][4]}\n\n"
                else:
                    result += f"{x}.{mashqlar[x-1][3]}\n♻️ {javob}\n✅ {mashqlar[x-1][4]}\n💡 <tg-spoiler>{izoh}</tg-spoiler>\n\n"
                x+=1
        izoh = mashqlar[x - 1][5]
        if izoh == 'yoq':
            result += f"{x}.{mashqlar[x - 1][3]}\n♻️ {message.text}\n✅ {mashqlar[x - 1][4]}\n\n"
        else:
            result += f"{x}.{mashqlar[x - 1][3]}\n♻️ {message.text}\n✅ {mashqlar[x - 1][4]}\n💡 <tg-spoiler>{izoh}</tg-spoiler>\n\n"
        await message.answer(f"Javoblar:\n\n{result}", reply_markup=menu)
        await state.finish()
        user = db.select_user(id=message.from_user.id)
        for ADMIN in ADMINS:
            await bot.send_message(chat_id=ADMIN, text=f"{user[1]} mashq bajardi\n\nFoydalanuvchi javoblari:\n\n{result}")
    else:
        if son < 10:
            if not javob1:
                await state.update_data(javob1=message.text)
            else:
                result = f"{javob1}/{message.text}"
                await state.update_data(javob1=result)
        elif son < 20:
            if not javob2:
                await state.update_data(javob2=message.text)
            else:
                result = f"{javob2}/{message.text}"
                await state.update_data(javob2=result)
        elif son < 30:
            if not javob3:
                await state.update_data(javob3=message.text)
            else:
                result = f"{javob3}/{message.text}"
                await state.update_data(javob3=result)
        elif son < 40:
            if not javob4:
                await state.update_data(javob4=message.text)
            else:
                result = f"{javob4}/{message.text}"
                await state.update_data(javob4=result)
        else:
            if not javob5:
                await state.update_data(javob5=message.text)
            else:
                result = f"{javob5}/{message.text}"
                await state.update_data(javob5=result)
        await message.answer(mashqlar[son][3])
        await state.update_data(son=f"{son+1}")


@dp.message_handler(text="👤 Shaxsiy kabinet")
async def shaxs_hand(message: Message):
    user = db.select_user(id=message.from_user.id)
    await message.answer(f"Ism: {user[1]}\n\n"
                         f"Telefon raqam: {user[2]}", reply_markup=edit_cabinet)

@dp.callback_query_handler(user_edit_kabinet_callback.filter())
async def edit_cabinet_hand(call: CallbackQuery, callback_data: dict):
    holat = callback_data.get('holat')
    if holat == 'ism':
        await edit_cabinet_state.ism.set()
        await call.message.delete()
        await call.message.answer("📌 Ismingizni to'liq kiriting:\n\n"
                                  "Misol uchun: Asqarov Alisher", reply_markup=ReplyKeyboardRemove())
    elif holat == 'telefon':
        await edit_cabinet_state.phone.set()
        await call.message.delete()
        await call.message.answer("📲 Telefon raqamni yuboring\n\nTelefon raqamni yuborish tugmasini bosing 👇",reply_markup=phone_num)

@dp.message_handler(state=edit_cabinet_state.ism)
async def edit_ism_hand(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("✅ Ism o'zgartirildi", reply_markup=menu)
    db.update_user_ism(fullname=message.text, id=message.from_user.id)

@dp.message_handler(state=edit_cabinet_state.phone, content_types=ContentTypes.CONTACT)
async def edit_phone_hand(message: Message, state: FSMContext):
    if message.contact:
        await message.answer("✅ Telefon raqam o'zgartirildi", reply_markup=menu)
        db.update_user_phone(phone=message.contact.phone_number, id=message.from_user.id)
        await state.finish()
    else:
        try:
            int(message.text)
            text = message.text
            if text.startswith('+998') and len(text) == 13:
                await message.answer("✅ Telefon raqam o'zgartirildi", reply_markup=menu)
                db.update_user_phone(phone=message.contact.phone_number, id=message.from_user.id)
                await state.finish()
            else:
                await message.answer("⚠️ Iltimos O'zbekiston telefon raqamini kiriting: +998991234567")
        except:
            await message.answer("⚠️ Telefon raqamni sonlarda kiriting\n\nMisol uchun: +998991234567")