from aiogram import types


def select_type_of_service():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='Yetkazib berish🚚', callback_data='delivery'))
    keyboard.add(types.InlineKeyboardButton(text='Olib ketish🥡', callback_data='takeout'))
    keyboard.add(types.InlineKeyboardButton(text='Ortga qaytish', callback_data='back_to_main'))
    return keyboard


def verify_location():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text='✅ Tasdiqlash', callback_data='verify_location'),
            types.InlineKeyboardButton(text='🔄️Qayta yuborish', callback_data='request_location')
        ]
    ])
