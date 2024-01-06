from aiogram import types

from loader import cart, afc


def cart_keyboard(user_id):
    global modificator_name
    cart_items = cart.get_cart(user_id=user_id)

    keyboard = types.InlineKeyboardMarkup(row_width=4)

    products = afc.get_products()
    product_dict = {}
    price = ''
    for product in products:
        product_dict[product['product_id']] = product

    for cart_item in cart_items:
        modificator_name = ''
        product = product_dict[f"{cart_item.product_id}"]
        if cart_item.modificator_id is None:
            price = f"{product['spots'][0]['price']}"[:-2]
        else:
            if 'modifications' in product:
                for modification in product['modifications']:
                    if modification['modificator_id'] == str(cart_item.modificator_id):
                        price = f"{modification['spots'][0]['price']}"[:-2]
                        modificator_name = f"{modification['modificator_name']}"
                        break
            elif 'group_modifications' in product:
                for modification in product['group_modifications'][0]['modifications']:
                    if modification['dish_modification_id'] == int(cart_item.modificator_id):
                        price = f"{modification['price']}"
                        modificator_name = f"{modification['name']}"
                        break

        keyboard.add(
            types.InlineKeyboardButton(
                text=f"{product['product_name']} {modificator_name} {price}so'm",
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
