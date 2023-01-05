from aiogram.types import CallbackQuery
from keyboards.inline.sponsor_inline import sponsor_keyboard
from loader import dp, _


@dp.callback_query_handler(text="sponsors")
async def show_sponsors(call: CallbackQuery):
    await call.message.edit_text(_("Наш проект работает на <b>Open Source</b> и мы будем рады,"
                                   "если вы нам поможете развивать проект.\n\n"
                                   "С помощью кнопки <b>💰 Донат</b> вы можете отправить своё пожертвование"),
                                 reply_markup=await sponsor_keyboard())
