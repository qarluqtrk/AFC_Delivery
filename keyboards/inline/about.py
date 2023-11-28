from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def back():
    return InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬅️Orqaga', callback_data='back'))