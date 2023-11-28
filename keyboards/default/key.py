from aiogram import types


def request_phone_number():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text="Raqamni yuborish", request_contact=True)
    keyboard.add(button)
    return keyboard


def request_location():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text="Manzilni yuborish", request_location=True)
    button1 = types.KeyboardButton(text="Ortga")
    keyboard.add(button, button1)
    return keyboard
