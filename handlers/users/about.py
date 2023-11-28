from aiogram import types

from keyboards.inline.about import back
from loader import dp


@dp.callback_query_handler(text='about')
async def about(call: types.CallbackQuery):
    photo_path = 'images/afc_hall.jpg'
    with open(photo_path, 'rb') as photo:
        await call.message.edit_media(media=types.InputMediaPhoto(photo,
                                                                  caption='🍔Endi Qarshi shahrida o’zgacha va yagona '
                                                                          'ta’mlar\n'
                                                                          "🏢AFC 2021-yildan beri o'z faoliyatini "
                                                                          "yuritadi"))
        await call.message.edit_reply_markup(reply_markup=back())
