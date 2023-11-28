from aiogram import types


def select_type_of_service():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text='Yetkazib berish🚚', callback_data='delivery'),
            types.InlineKeyboardButton(text='Oib ketish🥡', callback_data='takeout'),
            types.InlineKeyboardButton(text='Ortga qaytish', callback_data='back_to_main')
        ]
    ])


def verify_location():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text='✅ Tasdiqlash', callback_data='verify_location'),
            types.InlineKeyboardButton(text='🔄️Qayta yuborish', callback_data='request_location')
        ]
    ])