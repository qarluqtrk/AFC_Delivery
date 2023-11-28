from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import cart


def start_keyboard(user_id):
    keyboard = InlineKeyboardMarkup(row_width=2)

    menu_button = InlineKeyboardButton("Menu😋", callback_data='menu')
    if cart.check(user_id=user_id):
        cart_button = InlineKeyboardButton("Savatcha🛒", callback_data='cart')
        keyboard.add(cart_button)
    about_button = InlineKeyboardButton("Biz haqimizdaℹ️", callback_data='about')
    contact_button = InlineKeyboardButton("Biz bilan bog'lanish☎️", callback_data='contact')

    keyboard.add(menu_button, about_button, contact_button)
    return keyboard
