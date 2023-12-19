from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import afc

categories = afc.get_categories()


def categories_key():
    keyboard = InlineKeyboardMarkup()
    for category in categories:
        keyboard.add(InlineKeyboardMarkup(text=category['category_name'], callback_data=category['category_id']))
    keyboard.add(InlineKeyboardMarkup(text="🔙Ortga qaytish", callback_data="back_to_main"))
    return keyboard


def products_key(category_id):
    keyboard = InlineKeyboardMarkup()
    products = afc.get_products(category_id)
    for product in products:
        keyboard.add(InlineKeyboardMarkup(text=product['product_name'], callback_data=product['product_id']))
    keyboard.add(InlineKeyboardMarkup(text="🔙Ortga qaytish", callback_data="back_to_categories"))
    return keyboard


def booking_key(quantity):
    keyboard = InlineKeyboardMarkup(row_width=3)
    if quantity > 1:
        keyboard.add(InlineKeyboardButton(text="-", callback_data="minus"))
    keyboard.add(InlineKeyboardButton(text=f"{quantity}", callback_data=f"{quantity}"))
    keyboard.add(InlineKeyboardButton(text="+", callback_data="plus"))
    keyboard.add(InlineKeyboardButton(text="Savatga qo'shish🛒", callback_data="booking"))
    keyboard.add(InlineKeyboardButton(text="🔙Ortga qaytish", callback_data="back_to_products"))
    return keyboard


def choose_modification_key(modifications):
    keyboard = InlineKeyboardMarkup(row_width=3)
    for modification in modifications:
        keyboard.add(
            InlineKeyboardButton(text=f"{modification['modificator_name']} - {modification['spots'][0]['price']}",
                                 callback_data=modification['modificator_id']))
    keyboard.add(InlineKeyboardButton(text="🔙Ortga qaytish", callback_data="back_to_products"))
    return keyboard


def dish_modification_key(modifications):
    keyboard = InlineKeyboardMarkup()
    for modification in modifications:
        keyboard.add(InlineKeyboardButton(text=f"{modification['name']} - {modification['price']}",
                                          callback_data=modification['dish_modification_id']))
    keyboard.add(InlineKeyboardButton(text="🔙Ortga qaytish", callback_data="back_to_products"))
    return keyboard
