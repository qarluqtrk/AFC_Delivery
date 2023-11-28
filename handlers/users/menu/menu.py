from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import bot_start
from keyboards.inline.menu import categories_key, products_key, booking_key
from keyboards.inline.start import start_keyboard
from loader import dp, afc, bot, cart
from states.menu import MenuState


@dp.callback_query_handler(text="menu")
async def menu(call: types.CallbackQuery):
    await call.message.edit_caption("Bo'limni tanlang", reply_markup=categories_key())
    await MenuState.categories.set()


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


@dp.callback_query_handler(state=MenuState.product)
async def choose_product(call: types.CallbackQuery, state: FSMContext):
    if call.data != 'back_to_categories':
        product = afc.get_product(call.data)
        async with state.proxy() as data:
            data['quantity']: int = 1
            data['product_id'] = call.data
        await call.message.answer_photo(photo=afc.base_url + product['photo'] + '?token=' + afc.api_key,
                                        caption=f"{product['product_name']}\n"
                                                # f"{product['product_production_description']}\n"
                                                f"{product['spots'][0]['price'][:-2]} so'm",
                                        reply_markup=booking_key(data['quantity']))
        await MenuState.booking.set()
        await call.message.delete()
    else:
        await menu(call)


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
            if cart.check(call.from_user.id, data['product_id']):
                photo_path = 'images/afc-logo.png'
                with open(photo_path, 'rb') as photo:
                    await call.message.edit_media(
                        media=types.InputMediaPhoto(media=photo, caption="Bu mahsulot sizning savatingizda bor"))
                    await call.message.edit_reply_markup(reply_markup=start_keyboard(user_id=call.from_user.id))
                    await state.finish()
            else:
                cart.add_to_cart(call.from_user.id, data['product_id'], data['quantity'])
                photo_path = 'images/afc-logo.png'
                with open(photo_path, 'rb') as photo:
                    await call.message.edit_media(media=types.InputMediaPhoto(media=photo, caption="Savatchaga qo'shildi"))
                    await call.message.edit_reply_markup(reply_markup=start_keyboard(user_id=call.from_user.id))
                    await state.finish()
    elif call.data == 'back_to_products':
        photo_path = 'images/afc-logo.png'
        with open(photo_path, 'rb') as photo:
            await call.message.edit_media(media=types.InputMediaPhoto(media=photo))
            await menu(call)


