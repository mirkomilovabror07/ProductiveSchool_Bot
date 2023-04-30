import os
import xlsxwriter as xl
import asyncio
from aiogram.types import Message, CallbackQuery, ContentTypes, InputFile
from loader import db, dp, bot
from keyboards.inline.admin_keyboard import admin_Panel, admin_menu_callback,add_mashq_callback, add_level_callback, add_mashqkey, add_for_level, add_savol_callback, add_savol, izoh_yoqkey, savol_edit_key, savol_edit_callback, adminlar_callback, adminlar_key
from aiogram.dispatcher import FSMContext
from states.add_mashq import add_mashq_state, add_savol_state, edit_savol_state
from states.sendAd import send_reklama
from states.add_admin_state import addadmin_state

@dp.callback_query_handler(admin_menu_callback.filter())
async def menu(call: CallbackQuery, callback_data: dict):
    holat = callback_data.get('holat')
    if holat == "mashq":
        await call.message.edit_text(text="Qaysi darajaga mashq qo'shmoqchi bo'lsangiz tanlang 👇", reply_markup=add_for_level)
    elif holat == "statik":
        son = db.count_users()
        await call.answer(f"Botda foydalanuvchilar: {son[0]} ta", show_alert=True)
    elif holat == 'reklama':
        await send_reklama.send.set()
        await call.message.delete()
        await call.message.answer("📣 Reklama yuborishingiz mumkin")
    elif holat == 'admin':
        key = await adminlar_key()
        await call.message.edit_text(text="⚠️ Adminlar ro'yxatidan adminni o'chirmoqchi bo'lsangiz admin ustiga bosing", reply_markup=key)
    elif holat == 'user':
        users = db.select_all_users()
        workbook = xl.Workbook("users.xlsx")
        bold_format = workbook.add_format({'bold': True})
        worksheet = workbook.add_worksheet("Users")
        worksheet.write('A1', 'Ism', bold_format)
        worksheet.write('B1', 'Telefon raqam', bold_format)
        worksheet.write('C1', 'Telegram id', bold_format)
        rowIndex = 2
        for user in users:
            username = user[1]
            tel = user[2]
            tg_id = user[0]
            worksheet.write('A' + str(rowIndex), username)
            worksheet.write('B' + str(rowIndex), tel)
            worksheet.write('C' + str(rowIndex), tg_id)
            rowIndex += 1
        workbook.close()
        file = InputFile(path_or_bytesio="users.xlsx")
        await call.message.answer_document(document=file, caption="Userlar ro'yxati")
        os.remove(path="users.xlsx")

@dp.callback_query_handler(add_level_callback.filter())
async def add_level(call: CallbackQuery, callback_data: dict):
    level = callback_data.get('level')
    if level == 'orqaga':
        await call.message.edit_text("👮🏻‍♂️ Admin panelga xush kelibsiz!", reply_markup=admin_Panel)
    else:
        key = add_mashqkey(level=level)
        await call.message.edit_text("Mashq ichiga savol qo'shmoqchi bo'lsangiz kerakli mashqni tanlang!\n\n"
                                     "Yangi mashq qo'shish uchun Mashq qo'shish tugmasini boshing", reply_markup=key)

@dp.callback_query_handler(add_mashq_callback.filter())
async def add_mashq(call: CallbackQuery, state: FSMContext, callback_data: dict):
    level = callback_data.get('level')
    mashq = callback_data.get('mashq')
    if mashq == 'add_mashq':
        await state.update_data(level=level)
        await call.message.delete()
        await call.message.answer("📌 Mashqni nomini kiriting:")
        await add_mashq_state.mashq.set()
    elif mashq == 'orqaga':
        await call.message.edit_text(text="Qaysi darajga mashq qo'shmoqchi bo'lsangiz tanlang 👇",reply_markup=add_for_level)
    else:
        key = add_savol(level=level, mashq=mashq)
        await call.message.edit_text(text=f"Savol qo'shmoqchi bo'lsangiz qo'shish ustiga boshing!", reply_markup=key)

@dp.message_handler(state=add_mashq_state.mashq)
async def addmashqnomi(message: Message, state: FSMContext):
    async with state.proxy() as data:
        level = data.get('level')
    db.add_keyboard(types=level, text=message.text)
    key = add_mashqkey(level=level)
    await state.finish()
    await message.answer("Mashq ichiga savol qo'shmoqchi bo'lsangiz kerakli mashqni tanlang!\n\nYangi mashq qo'shish uchun Mashq qo'shish tugmasini boshing", reply_markup=key)

@dp.callback_query_handler(add_savol_callback.filter())
async def add_savol_hand(call: CallbackQuery, state: FSMContext, callback_data: dict):
    level = callback_data.get('level')
    mashq = callback_data.get('mashq')
    id = callback_data.get('id')
    if id == 'orqaga':
        key = add_mashqkey(level=level)
        await call.message.edit_text("Mashq ichiga savol qo'shmoqchi bo'lsangiz kerakli mashqni tanlang!\n\n""Yangi mashq qo'shish uchun qosh tugmasini boshing ⚠️",reply_markup=key)
    elif id == 'add_savol':
        await state.update_data(level=level)
        await state.update_data(mashq=mashq)
        await add_savol_state.savol.set()
        await call.message.delete()
        await call.message.answer("📌 Savolni kiriting:")
    else:
        key = savol_edit_key(level=level, mashq=mashq, id=id)
        savol = db.select_mashq(id=id)
        await call.message.edit_text(text=f"Savol : {savol[3]}\n\nJavob: {savol[4]}\n\nIzoh: {savol[5]}", reply_markup=key)

@dp.message_handler(state=add_savol_state.savol)
async def add_savol_state_hand(message: Message, state: FSMContext):
    await state.update_data(savol=message.text)
    await message.answer("📌 Javobni kiriting:")
    await add_savol_state.javob.set()

@dp.message_handler(state=add_savol_state.javob)
async def add_savol_state_hand(message: Message, state: FSMContext):
    await state.update_data(javob=message.text)
    await message.answer("📌 Izohni kiriting:", reply_markup=izoh_yoqkey)
    await add_savol_state.izoh.set()

@dp.message_handler(state=add_savol_state.izoh)
async def add_savol_state_hand(message: Message, state: FSMContext):
    async with state.proxy() as data:
        level = data.get('level')
        mashq = data.get('mashq')
        savol = data.get('savol')
        javob = data.get('javob')
        db.add_mashq(daraja=level, mashq=mashq, savol=savol, javob=javob, izoh=message.text)
        key = add_savol(level=level, mashq=mashq)
        await message.answer(text=f"Savol qo'shmoqchi bo'lsangiz qo'shish ustiga boshing!", reply_markup=key)
        await state.finish()

@dp.callback_query_handler(state=add_savol_state.izoh, text='yoq')
async def izohyoqhand(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        level = data.get('level')
        mashq = data.get('mashq')
        savol = data.get('savol')
        javob = data.get('javob')
    await call.message.delete()
    db.add_mashq(daraja=level, mashq=mashq, savol=savol, javob=javob, izoh='yoq')
    key = add_savol(level=level, mashq=mashq)
    await call.message.answer(text=f"Savol qo'shmoqchi bo'lsangiz qo'shish ustiga boshing!", reply_markup=key)
    await state.finish()

@dp.callback_query_handler(savol_edit_callback.filter())
async def savol_edit_hand(call: CallbackQuery, state: FSMContext, callback_data: dict):
    level = callback_data.get('level')
    mashq = callback_data.get('mashq')
    id = callback_data.get('id')
    holat = callback_data.get('holat')
    if holat == 'orqaga':
        key = add_savol(level=level, mashq=mashq)
        await call.message.edit_text(text=f"Savol qo'shmoqchi bo'lsangiz qo'shish ustiga boshing!", reply_markup=key)
    elif holat == 'savol':
        await state.update_data(level=level)
        await state.update_data(mashq=mashq)
        await state.update_data(id=id)
        await call.message.delete()
        await edit_savol_state.savol.set()
        await call.message.answer("📌 Savolni kiriting:")
    elif holat == 'javob':
        await state.update_data(level=level)
        await state.update_data(mashq=mashq)
        await state.update_data(id=id)
        await call.message.delete()
        await edit_savol_state.javob.set()
        await call.message.answer("📌 Javobni kiriting:")
    elif holat == 'izoh':
        await state.update_data(level=level)
        await state.update_data(mashq=mashq)
        await state.update_data(id=id)
        await call.message.delete()
        await edit_savol_state.izoh.set()
        await call.message.answer("📌 Izohni kiriting:")

@dp.message_handler(state=edit_savol_state.savol)
async def edit_savol_state_hand(message: Message, state: FSMContext):
    async with state.proxy() as data:
        level = data.get('level')
        mashq = data.get('mashq')
        id = data.get('id')
    db.update_mashq_savol(savol=message.text, id=id)
    key = savol_edit_key(level=level, mashq=mashq, id=id)
    savol = db.select_mashq(id=id)
    await message.answer(text=f"Savol: {savol[3]}\n\nJavob: {savol[4]}\n\nIzoh: {savol[5]}", reply_markup=key)
    await state.finish()

@dp.message_handler(state=edit_savol_state.javob)
async def edit_savol_state_hand(message: Message, state: FSMContext):
    async with state.proxy() as data:
        level = data.get('level')
        mashq = data.get('mashq')
        id = data.get('id')
    db.update_mashq_javob(javob=message.text, id=id)
    key = savol_edit_key(level=level, mashq=mashq, id=id)
    savol = db.select_mashq(id=id)
    await message.answer(text=f"Savol: {savol[3]}\n\nJavob: {savol[4]}\n\nIzoh: {savol[5]}", reply_markup=key)
    await state.finish()

@dp.message_handler(state=edit_savol_state.izoh)
async def edit_savol_state_hand(message: Message, state: FSMContext):
    async with state.proxy() as data:
        level = data.get('level')
        mashq = data.get('mashq')
        id = data.get('id')
    db.update_mashq_izoh(izoh=message.text, id=id)
    key = savol_edit_key(level=level, mashq=mashq, id=id)
    savol = db.select_mashq(id=id)
    await message.answer(text=f"Savol: {savol[3]}\n\nJavob: {savol[4]}\n\nIzoh: {savol[5]}", reply_markup=key)
    await state.finish()


#Userlarga reklama yuborish qismi
@dp.message_handler(state=send_reklama.send, content_types=ContentTypes.ANY)
async def sendreklama_hand(message: Message, state: FSMContext):
    users = db.select_all_users()
    y = 0
    q = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0], from_chat_id=message.from_user.id, message_id=message.message_id)
            y += 1
        except:
            q += 1
            pass
        await asyncio.sleep(0.5)
    await message.answer(f"✅ Reklama yuborildi\n\nQabul qildi: {y} dona\n\nBlock: {q} dona")
    await message.answer("👮🏻‍♂️ Admin panelga xush kelibsiz!", reply_markup=admin_Panel)
    await state.finish()

@dp.callback_query_handler(adminlar_callback.filter())
async def adminlar_hand(call: CallbackQuery, callback_data: dict):
    id = callback_data.get('id')
    if id == 'add':
        await addadmin_state.admin.set()
        await call.message.delete()
        await call.message.answer("⚠️ Qo'shmoqchi bo'lgan adminning telegram ID sini jo'nating")
    elif id == 'orqaga':
        await call.message.edit_text("👮🏻‍♂️ Admin panelga xush kelibsiz!", reply_markup=admin_Panel)
    else:
        id = int(id)
        db.delete_admin(id=id)
        key = await adminlar_key()
        await call.message.edit_reply_markup(reply_markup=key)

@dp.message_handler(state=addadmin_state.admin)
async def add_admin_hand(message: Message, state: FSMContext):
    await state.finish()
    try:
        user = await bot.get_chat(chat_id=message.text)
        db.add_admin(id=user.id)
        await message.answer("✅ Admin qo'shildi")
    except:
        await message.answer("❗ Admin topilmadi")