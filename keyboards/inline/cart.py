from aiogram import types
from aiogram.types import InlineKeyboardMarkup

from loader import cart, afc

import time


def cart_keyboard(user_id):
    cart_items = cart.get_cart(user_id=user_id)

    keyboard = types.InlineKeyboardMarkup(row_width=4)

    products = afc.get_products()
    product_dict = {}
    for product in products:
        product_dict[product['product_id']] = product

    for cart_item in cart_items:
        product = product_dict[f"{cart_item.product_id}"]
        price = f"{product['spots'][0]['price']}"[:-2]

        keyboard.add(
            types.InlineKeyboardButton(
                text=f"{product['product_name']} {price}so'm",
                callback_data=cart_item.id
            ))

        keyboard.add(
            types.InlineKeyboardButton(
                text="-",
                callback_data=f"minus - {cart_item.id}"
            ),
            types.InlineKeyboardButton(
                text=f"{cart_item.quantity}",
                callback_data="quantity"
            ),
            types.InlineKeyboardButton(
                text="+",
                callback_data=f"plus - {cart_item.id}"
            ),
            types.InlineKeyboardButton(
                text="❌",
                callback_data=f"delete - {cart_item.id}"
            )
        )

    keyboard.add(types.InlineKeyboardButton(text='Buyurtma Berish📦', callback_data='order'))

    keyboard.add(types.InlineKeyboardButton(text='Savatni tozalash🧹', callback_data='clear_cart'),
                 types.InlineKeyboardButton(text='Ortga qaytish', callback_data='back_to_main'))
    return keyboard

