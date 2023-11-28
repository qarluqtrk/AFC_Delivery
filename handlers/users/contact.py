from aiogram import types

from keyboards.inline.contact import contact
from keyboards.inline.start import start_keyboard
from loader import dp


@dp.callback_query_handler(text='contact')
async def bot_start(call: types.CallbackQuery):
    await call.message.edit_caption("📍Manzil: Eski gilam bozori, Mo'ljal: Ona haykali\n"
                                    "☎️Tel: +998882281003",
                                    reply_markup=contact())


@dp.callback_query_handler(text='back')
async def back(call: types.CallbackQuery):
    photo_path = 'images/afc-logo.png'
    with open(photo_path, 'rb') as photo:
        await call.message.edit_media(media=types.InputMediaPhoto(photo, "Assalomu Alaykum!\n"
                                                                         "AFC ga xush kelibsiz!\n"
                                                                         "Sizni menyu bilan tanishtirishim, buyurtma "
                                                                         "olishim va joy band qilishingizga yordam "
                                                                         "berishim mumkin\n"
                                                                         "Davom etish uchun quyidagi tugmalardan "
                                                                         "birini bosing👇👇"))
        await call.message.edit_reply_markup(reply_markup=start_keyboard(user_id=call.from_user.id))
