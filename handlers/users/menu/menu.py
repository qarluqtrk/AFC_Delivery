from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.menu import categories_key, products_key, booking_key, choose_modification_key
from keyboards.inline.start import start_keyboard
from loader import dp, afc, cart
from states.menu import MenuState

"""
Components
"""

photo_path = 'images/afc-logo.png'

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


#
# @dp.callback_query_handler(state=MenuState.product)
# async def choose_product(call: types.CallbackQuery, state: FSMContext):
#     if call.data != 'back_to_categories':
#         product = afc.get_product(call.data)
#         await call.message.delete()
#         async with state.proxy() as data:
#             data['quantity']: int = 1
#             data['product_id'] = call.data
#             try:
#                 try:
#                     await MenuState.modifications.set()
#                     await call.message.answer_photo(photo=afc.base_url + product['photo'] + '?token=' + afc.api_key,
#                                                     caption=f"{product['product_name']}\n",
#                                                     reply_markup=choose_modification_key(
#                                                         modifications=product['modifications']))
#                 except:
#                     await MenuState.modifications.set()
#                     await call.message.answer_photo(photo=afc.base_url + product['photo'] + '?token=' + afc.api_key,
#                                                     caption=f"{product['product_name']}\n",
#                                                     reply_markup=dish_modification_key(
#                                                         product['group_modifications'][0]['modifications']))
#             except:
#                 await call.message.answer_photo(photo=afc.base_url + product['photo'] + '?token=' + afc.api_key,
#                                                 caption=f"{product['product_name']}\n"
#                                                 # f"{product['product_production_description']}\n"
#                                                         f"{product['spots'][0]['price'][:-2]} so'm",
#                                                 reply_markup=booking_key(data['quantity']))
#                 await MenuState.booking.set()
#
#
#     else:
#         await menu(call)


@dp.callback_query_handler(state=MenuState.product)
async def choose_product(call: types.CallbackQuery, state: FSMContext):
    if call.data != 'back_to_categories':
        async with state.proxy() as data:
            data['quantity']: int = 1
            data['product_id'] = call.data
            product = afc.get_product(call.data)
            if 'modifications' in product:
                await call.message.answer_photo(photo=afc.base_url + product['photo'],
                                                caption=f"{product['product_name']}\n",
                                                reply_markup=choose_modification_key(
                                                    modifications=product['modifications'],
                                                    type='modifications'))
                await call.message.delete()
                await MenuState.modifications.set()
            elif 'group_modifications' in product:
                if len(product['group_modifications']) == 1:
                    if product['group_modifications'][0]['type'] == 1:
                        await call.message.answer_photo(photo=afc.base_url + product['photo'],
                                                        caption=f"{product['product_name']}\n",
                                                        reply_markup=choose_modification_key(
                                                            modifications=product['group_modifications'][0][
                                                                'modifications'],
                                                            type='group_modifications'
                                                        ))
                        await call.message.delete()
                        await MenuState.modifications.set()
                    else:
                        if product['group_modifications'][0]['num_min'] != product['group_modifications'][0]['num_max']:
                            await call.message.answer_photo(photo=afc.base_url + product['photo'],
                                                            caption=f"{product['product_name']}\n\n\n",
                                                            reply_markup=choose_modification_key(
                                                                modifications=product['group_modifications'][0][
                                                                    'modifications'],
                                                                type='group_modifications'
                                                            ))
                            await call.message.delete()
                            await MenuState.modifications.set()
                        else:
                            caption = ''
                            caption += f"{product['product_name']}\n"
                            caption += f"Narxi: <b>{product['sources'][1]['price'][:-2]}</b>\n\n\n"
                            caption += f"Combo Quyidagilarni o'z ichiga oladi:\n\n"
                            count = 1
                            for combo_item in product['group_modifications'][0]['modifications']:
                                caption += f"{count}.{combo_item['name']} - {combo_item['brutto']}ta\n"
                                count += 1
                            await call.message.answer_photo(photo=afc.base_url + product['photo'],
                                                            caption=caption,
                                                            reply_markup=booking_key(data['quantity']))
                            await call.message.delete()
                            await MenuState.booking.set()
                else:
                    caption = ''
                    caption += f"{product['product_name']}\n"
                    caption += f"Narxi: <b>{product['sources'][1]['price'][:-2]}</b>\n\n\n"
                    caption += f"Combo Quyidagilarni o'z ichiga oladi:\n\n"
                    count = 1
                    for combo_item in product['group_modifications']:
                        caption += f"{count}.{combo_item['modifications'][0]['name']} - {combo_item['modifications'][0]['brutto']}ta\n"
                        count += 1
                    await call.message.answer_photo(photo=afc.base_url + product['photo'],
                                                    caption=caption,
                                                    reply_markup=booking_key(data['quantity']))
                    await call.message.delete()
                    await MenuState.booking.set()
            else:
                await call.message.answer_photo(photo=afc.base_url + product['photo'] + '?token=' + afc.api_key,
                                                caption=f"{product['product_name']}\n"
                                                # f"{product['product_production_description']}\n"
                                                        f"{product['spots'][0]['price'][:-2]} so'm",
                                                reply_markup=booking_key(data['quantity']))
                await MenuState.booking.set()
    else:
        await state.finish()
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
            if 'modifications' in product:
                for modification in product['modifications']:
                    if modification['modificator_id'] == call.data:
                        price = modification['sources'][1]['price'][:-2]
                        break
            elif "group_modifications" in product:
                for modification in product['group_modifications'][0]['modifications']:
                    if modification['dish_modification_id'] == int(call.data):
                        price = modification['price']
                        break
            await call.message.edit_caption(caption=f"{product['product_name']}\n"
                                                    f"{price} so'm",
                                            reply_markup=booking_key(data['quantity']))
            await MenuState.booking.set()
    else:
        await state.finish()
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
            if 'modificator_id' in data:
                if cart.check(call.from_user.id, data['product_id'], data['modificator_id']):

                    with open(photo_path, 'rb') as photo:
                        await call.message.edit_media(
                            media=types.InputMediaPhoto(media=photo, caption="Bu mahsulot sizning savatingizda bor"))
                        await call.message.edit_reply_markup(reply_markup=start_keyboard(user_id=call.from_user.id))
                        await state.finish()
                else:
                    cart.add_to_cart_modificator(user_id=call.from_user.id, product_id=data['product_id'],
                                                 modificator_id=data['modificator_id'], quantity=data['quantity'])

                    with open(photo_path, 'rb') as photo:
                        await call.message.edit_media(
                            media=types.InputMediaPhoto(media=photo, caption="Savatchaga qo'shildi"))
                        await call.message.edit_reply_markup(reply_markup=start_keyboard(user_id=call.from_user.id))
                        await state.finish()
            else:
                if cart.check(call.from_user.id, data['product_id']):

                    with open(photo_path, 'rb') as photo:
                        await call.message.edit_media(
                            media=types.InputMediaPhoto(media=photo, caption="Bu mahsulot sizning savatingizda bor"))
                        await call.message.edit_reply_markup(reply_markup=start_keyboard(user_id=call.from_user.id))
                        await state.finish()
                else:
                    cart.add_to_cart(user_id=call.from_user.id, product_id=data['product_id'],
                                     quantity=data['quantity'])

                    with open(photo_path, 'rb') as photo:
                        await call.message.edit_media(
                            media=types.InputMediaPhoto(media=photo, caption="Savatchaga qo'shildi"))
                        await call.message.edit_reply_markup(reply_markup=start_keyboard(user_id=call.from_user.id))
                        await state.finish()
            # try:
            #     a = data['modificator_id']
            # except:
            #     data['modificator_id'] = None
            # if cart.check(call.from_user.id, data['product_id'], data['modificator_id']):
            #
            #     with open(photo_path, 'rb') as photo:
            #         await call.message.edit_media(
            #             media=types.InputMediaPhoto(media=photo, caption="Bu mahsulot sizning savatingizda bor"))
            #         await call.message.edit_reply_markup(reply_markup=start_keyboard(user_id=call.from_user.id))
            #         await state.finish()
            # else:
            #     try:
            #         cart.add_to_cart_modificator(call.from_user.id, data['product_id'], data['modificator_id'],
            #                                      data['quantity'])
            #     except:
            #         cart.add_to_cart(call.from_user.id, data['product_id'], data['quantity'])
            #
            #
            #     with open(photo_path, 'rb') as photo:
            #         await call.message.edit_media(
            #             media=types.InputMediaPhoto(media=photo, caption="Savatchaga qo'shildi"))
            #         await call.message.edit_reply_markup(reply_markup=start_keyboard(user_id=call.from_user.id))
            #         await state.finish()
    elif call.data == 'back_to_products':

        with open(photo_path, 'rb') as photo:
            await call.message.edit_media(media=types.InputMediaPhoto(media=photo))
            await menu(call)
