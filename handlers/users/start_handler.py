import asyncio
import random

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import BadRequest

from data.config import load_config
from filters import IsPrivate
from functions.app_scheduler import send_message_week
from functions.auxiliary_tools import registration_menu
from handlers.users.back_handler import delete_message
from keyboards.inline.language_inline import language_keyboard

from keyboards.inline.main_menu_inline import start_keyboard
from loader import dp, scheduler, _
from utils.db_api import db_commands


@dp.message_handler(IsPrivate(), CommandStart())
async def register_user(message: types.Message):
    try:
        if message.from_user.username is not None:
            await db_commands.add_user(name=message.from_user.full_name,
                                       telegram_id=message.from_user.id,
                                       username=message.from_user.username)
            await db_commands.add_meetings_user(telegram_id=message.from_user.id,
                                                username=message.from_user.username)
        else:
            await db_commands.add_user(name=message.from_user.full_name,
                                       telegram_id=message.from_user.id,
                                       username="None")
            await db_commands.add_meetings_user(telegram_id=message.from_user.id,
                                                username="None")

    except:
        pass
    support = await db_commands.select_user(telegram_id=load_config().tg_bot.support_ids[0])
    user_db = await db_commands.select_user(telegram_id=message.from_user.id)
    markup = await start_keyboard(status=user_db["status"])
    fullname = message.from_user.full_name

    heart = random.choice(['π', 'π', 'π', 'π§‘', 'π', 'π€', 'β€', 'π€', 'π', 'π'])
    await message.answer(_("ΠΡΠΈΠ²Π΅ΡΡΡΠ²ΡΡ Π²Π°Ρ, {fullname}!!\n\n"
                           "{heart} <b> QueDateBot </b> - ΠΏΠ»Π°ΡΡΠΎΡΠΌΠ° Π΄Π»Ρ ΠΏΠΎΠΈΡΠΊΠ° Π½ΠΎΠ²ΡΡ Π·Π½Π°ΠΊΠΎΠΌΡΡΠ².\n\n"
                           "πͺ§ ΠΠΎΠ²ΠΎΡΡΠΈ ΠΎ ΠΏΡΠΎΠ΅ΠΊΡΠ΅ Π²Ρ ΠΌΠΎΠΆΠ΅ΡΠ΅ ΠΏΡΠΎΡΠΈΡΠ°ΡΡ Π² Π½Π°ΡΠ΅ΠΌ ΠΊΠ°Π½Π°Π»Π΅ - "
                           "https://t.me/QueDateGroup \n\n"
                           "<b>π€ Π‘ΠΎΡΡΡΠ΄Π½ΠΈΡΠ΅ΡΡΠ²ΠΎ: </b>\n"
                           "ΠΡΠ»ΠΈ Ρ Π²Π°Ρ Π΅ΡΡΡ ΠΏΡΠ΅Π΄Π»ΠΎΠΆΠ΅Π½ΠΈΠ΅ ΠΎ ΡΠΎΡΡΡΠ΄Π½ΠΈΡΠ΅ΡΡΠ²Π΅, ΠΏΠΈΡΠΈΡΠ΅ Π°Π³Π΅Π½ΡΡ ΠΏΠΎΠ΄Π΄Π΅ΡΠΆΠΊΠΈ - "
                           "@{supports}\n\n").format(fullname=fullname, heart=heart,
                                                     supports=support['username']),
                         reply_markup=markup)


@dp.callback_query_handler(text="start_menu")
async def start_menu(call: CallbackQuery):
    await registration_menu(call, scheduler, send_message_week, load_config, start_keyboard, random)


@dp.callback_query_handler(text="language")
@dp.callback_query_handler(text="language_reg")
async def choice_language(call: CallbackQuery):
    if call.data == "language_reg":
        try:
            await call.message.edit_text(_("ΠΡΠ±Π΅ΡΠΈΡΠ΅ ΡΠ·ΡΠΊ"), reply_markup=await language_keyboard("registration"))
        except BadRequest:
            await delete_message(call.message)
            await call.message.answer(_("ΠΡΠ±Π΅ΡΠΈΡΠ΅ ΡΠ·ΡΠΊ"), reply_markup=await language_keyboard("registration"))
    elif call.data == "language":
        try:
            await call.message.edit_text(_("ΠΡΠ±Π΅ΡΠΈΡΠ΅ ΡΠ·ΡΠΊ"), reply_markup=await language_keyboard("profile"))
        except BadRequest:
            await delete_message(call.message)
            await call.message.answer(_("ΠΡΠ±Π΅ΡΠΈΡΠ΅ ΡΠ·ΡΠΊ"), reply_markup=await language_keyboard("profile"))


@dp.callback_query_handler(text="Russian")
@dp.callback_query_handler(text="Deutsch")
@dp.callback_query_handler(text="English")
@dp.callback_query_handler(text="Indonesian")
async def change_language(call: CallbackQuery):
    if call.data == "Russian":
        await db_commands.update_user_data(telegram_id=call.from_user.id, language="ru")
    elif call.data == "Deutsch":
        await db_commands.update_user_data(telegram_id=call.from_user.id, language="de")
    elif call.data == "English":
        await db_commands.update_user_data(telegram_id=call.from_user.id, language="en")
    elif call.data == "Indonesian":
        await db_commands.update_user_data(telegram_id=call.from_user.id, language="in")
    await call.answer(_("Π―Π·ΡΠΊ Π±ΡΠ» ΡΡΠΏΠ΅ΡΠ½ΠΎ ΠΈΠ·ΠΌΠ΅Π½Π΅Π½. ΠΠ²Π΅Π΄ΠΈΡΠ΅ ΠΊΠΎΠΌΠ°Π½Π΄Ρ /start"), show_alert=True)
    await asyncio.sleep(5)
    await call.message.delete()
