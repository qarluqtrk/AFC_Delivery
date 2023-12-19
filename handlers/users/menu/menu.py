from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.menu import categories_key, products_key, booking_key, choose_modification_key, \
    dish_modification_key
from keyboards.inline.start import start_keyboard
from loader import dp, afc, cart
from states.menu import MenuState

"""
Menu categories list
"""


@dp.callback_query_handler(text="menu")
async def menu(call: types.CallbackQuery):
    await call.message.edit_caption("Bo'limni tanlang", reply_markup=categories_key())
    await MenuState.categories.set()


"""
Menu products list
"""


@dp.callback_query_handler(state=MenuState.categories)
async def choose_category(call: types.CallbackQuery, state: FSMContext):
    if call.data != 'back_to_main':
        await call.message.edit_caption("Bo'limni tanlang", reply_markup=products_key(call.data))
        await MenuState.product.set()
    else:
        await state.finish()
        # await bot_start(message=call.message)
        await call.message.edit_caption("Assalomu Alaykum!\n"
                                        "AFC ga xush kelibsiz!\n"
                                        "Sizni menyu bilan tanishtirishim, buyurtma olishim va joy band qilishingizga yordam berishim mumkin\n"
                                        "Davom etish uchun quyidagi tugmalardan birini bosing👇👇",
                                        reply_markup=start_keyboard(user_id=call.from_user.id))


"""
Menu Product Info and modifications list
"""


@dp.callback_query_handler(state=MenuState.product)
async def choose_product(call: types.CallbackQuery, state: FSMContext):
    if call.data != 'back_to_categories':
        product = afc.get_product(call.data)
        print(product)
        await call.message.delete()
        async with state.proxy() as data:
            data['quantity']: int = 1
            data['product_id'] = call.data
            try:
                try:
                    await MenuState.modifications.set()
                    await call.message.answer_photo(photo=afc.base_url + product['photo'] + '?token=' + afc.api_key,
                                                    caption=f"{product['product_name']}\n",
                                                    reply_markup=choose_modification_key(
                                                        modifications=product['modifications']))
                except:
                    await MenuState.modifications.set()
                    await call.message.answer_photo(photo=afc.base_url + product['photo'] + '?token=' + afc.api_key,
                                                    caption=f"{product['product_name']}\n",
                                                    reply_markup=dish_modification_key(
                                                        product['group_modifications'][0]['modifications']))
            except:
                await call.message.answer_photo(photo=afc.base_url + product['photo'] + '?token=' + afc.api_key,
                                                caption=f"{product['product_name']}\n"
                                                # f"{product['product_production_description']}\n"
                                                        f"{product['spots'][0]['price'][:-2]} so'm",
                                                reply_markup=booking_key(data['quantity']))
                await MenuState.booking.set()


    else:
        await menu(call)


"""
Menu Modifications info and booking
"""


@dp.callback_query_handler(state=MenuState.modifications)
async def choose_modification(call: types.CallbackQuery, state: FSMContext):
    if call.data != 'back_to_products':
        async with state.proxy() as data:
            data['quantity']: int = 1
            data['modificator_id'] = call.data
            product = afc.get_product(data['product_id'])
            global price
            price = ''
            for modification in product['modifications']:
                if modification['modificator_id'] == call.data:
                    price = modification['spots'][0]['price']
                    break
            await call.message.edit_caption(caption=f"{product['product_name']}\n"
                                                    f"{price[:-2]} so'm",
                                            reply_markup=booking_key(data['quantity']))
            await MenuState.booking.set()
    else:
        await menu(call)


"""
Menu Booking
"""


@dp.callback_query_handler(state=MenuState.booking)
async def booking(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'plus':
        async with state.proxy() as data:
            data['quantity'] += 1
            await call.message.edit_reply_markup(reply_markup=booking_key(data['quantity']))
    elif call.data == 'minus':
        async with state.proxy() as data:
            data['quantity'] -= 1
            await call.message.edit_reply_markup(reply_markup=booking_key(data['quantity']))
    elif call.data == 'booking':
        async with state.proxy() as data:
            try:
                a = data['modificator_id']
            except:
                data['modificator_id'] = None
            if cart.check(call.from_user.id, data['product_id'], data['modificator_id']):
                photo_path = 'images/afc-logo.png'
                with open(photo_path, 'rb') as photo:
                    await call.message.edit_media(
                        media=types.InputMediaPhoto(media=photo, caption="Bu mahsulot sizning savatingizda bor"))
                    await call.message.edit_reply_markup(reply_markup=start_keyboard(user_id=call.from_user.id))
                    await state.finish()
            else:
                try:
                    cart.add_to_cart_modificator(call.from_user.id, data['product_id'], data['modificator_id'],
                                                 data['quantity'])
                except:
                    cart.add_to_cart(call.from_user.id, data['product_id'], data['quantity'])

                photo_path = 'images/afc-logo.png'
                with open(photo_path, 'rb') as photo:
                    await call.message.edit_media(
                        media=types.InputMediaPhoto(media=photo, caption="Savatchaga qo'shildi"))
                    await call.message.edit_reply_markup(reply_markup=start_keyboard(user_id=call.from_user.id))
                    await state.finish()
    elif call.data == 'back_to_products':
        photo_path = 'images/afc-logo.png'
        with open(photo_path, 'rb') as photo:
            await call.message.edit_media(media=types.InputMediaPhoto(media=photo))
            await menu(call)
