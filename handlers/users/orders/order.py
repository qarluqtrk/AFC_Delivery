from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import PROVIDER_TOKEN
from handlers.users.orders.cart import cart_view
from handlers.users.start import bot_start
from keyboards.default.key import request_location
from keyboards.inline.ordering import select_type_of_service
from keyboards.inline.start import start_keyboard
from loader import dp, bot, cart, afc
from states.menu import Checkout


@dp.callback_query_handler(state=Checkout.service_type)
async def service_type_view(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if call.data == 'delivery':
            data['service_type'] = 3
            data['request_location_message'] = await call.message.answer('Manzilni yuboring',
                                                                         reply_markup=request_location())
            await call.message.delete()
            await Checkout.location.set()
        elif call.data == 'takeout':
            data['service_type'] = 2
            await Checkout.payment.set()
            product = []
            for i in cart.get_cart(user_id=call.from_user.id):
                product.append({
                    'product_id': i.product_id,
                    'count': i.quantity
                })

                data['product'] = product.copy()
                data['cart_total'] = cart.cart_total(call.from_user.id)
            await call.message.delete()
            await bot.send_invoice(call.from_user.id,
                                   title='AFC Delivery',
                                   description='description',
                                   provider_token=PROVIDER_TOKEN,
                                   currency='UZS',
                                   need_phone_number=True,
                                   prices=[types.LabeledPrice(label="To'lovga", amount=data['cart_total'])],
                                   start_parameter='start_parameter',
                                   payload='test')
        else:
            await state.finish()
            await call.message.delete()
            photo_path = 'images/afc-logo.png'
            with open(photo_path, 'rb') as photo:
                await call.message.answer_photo(
                    photo=photo,
                    caption="Assalomu Alaykum!\n"
                            "AFC ga xush kelibsiz!\n"
                            "Sizni menyu bilan tanishtirishim, buyurtma olishim va joy band qilishingizga yordam berishim mumkin\n"
                            "Davom etish uchun quyidagi tugmalardan birini bosing👇👇",
                    reply_markup=start_keyboard(user_id=call.from_user.id))


@dp.pre_checkout_query_handler(lambda q: True, state=Checkout.payment)
async def checkout_process(pre_checkout_query: types.PreCheckoutQuery, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = "+" + pre_checkout_query.order_info.phone_number
        data['name'] = pre_checkout_query.order_info.name
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=types.ContentTypes.SUCCESSFUL_PAYMENT, state=Checkout.payment)
async def successful_payment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer("To'lov muvaffaqqiyatli amalga oshirildi")

        # Payment info

        data['payment'] = {
            'type': 1,
            'sum': cart.cart_total(message.from_user.id),
            'currency': 'UZS'
        }

        if data['service_type'] == 2:
            a = afc.create_takeout_order(phone=data['phone_number'],
                                         first_name=data['name'],
                                         payment=data['payment'],
                                         products=data['product'],
                                         service_type=2)
            if a:
                print(a)
                await message.answer("Buyurtma jo'natildi")
        else:
            a = afc.create_delivery_order(phone=data['phone_number'],
                                          first_name=data['name'],
                                          payment=data['payment'],
                                          products=data['product'],
                                          service_type=3,
                                          client_address=data['location'])
            if a:
                print(a)
                await message.answer("Buyurtma jo'natildi")

        # Clear cart
        cart.clear(user_id=message.from_user.id)
        with open("images/afc-logo.png", "rb") as photo:
            await message.answer_photo(photo=photo, caption="Savatingiz tozalandi",
                                       reply_markup=start_keyboard(message.from_user.id))
            await state.finish()
