from aiogram import types
from aiogram.dispatcher import FSMContext
from geopy import Nominatim

from data.config import PROVIDER_TOKEN
from handlers.users.start import bot_start
from keyboards.default.key import request_location
from keyboards.inline.ordering import verify_location
from loader import dp, bot, cart
from states.menu import Checkout


@dp.message_handler(state=Checkout.location, content_types=types.ContentType.LOCATION)
async def location_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        latitude = message.location.latitude
        longitude = message.location.longitude
        geolocator = Nominatim(user_agent="afc")
        location = geolocator.reverse((latitude, longitude), language='uz')
        client_address = {
            'address1': location.address,
            'lat': latitude,
            'lng': longitude,
            'comment': ''
        }
        data['location'] = client_address
        try:
            if location.raw['address']['city'] == 'Qarshi shahri':
                data['location_coordinates'] = await message.answer_location(latitude, longitude)
                await message.answer(f"Manzilingiz: {location.address}\n"
                                     f"Tasdiqlaysizmi", reply_markup=verify_location())
                await bot.delete_message(message.from_user.id, data['request_location_message'].message_id)
                await message.delete()
                await Checkout.location_check.set()
            else:
                await bot.delete_message(message.from_user.id, data['request_location_message'].message_id)
                await message.delete()
                data['request_location_message'] = await message.answer("Jo'natilgan manzil Qarshi shahri ichida emas\n"
                                                                        'Boshqa manzilni yuboring',
                                                                        reply_markup=request_location())

        except:
            await message.delete()
            await bot.delete_message(message.from_user.id, data['request_location_message'].message_id)
            data['request_location_message'] = await message.answer("Jo'natilgan manzil Qarshi shahri ichida emas\n"
                                                                    'Boshqa manzilni yuboring',
                                                                    reply_markup=request_location())


@dp.message_handler(state=Checkout.location, content_types=types.ContentType.TEXT)
async def location_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Ortga':
            await message.delete()
            await bot.delete_message(message.from_user.id, data['request_location_message'].message_id)
            await state.finish()
            await bot_start(message)
        else:
            await message.delete()
            await bot.delete_message(message.from_user.id, data['request_location_message'].message_id)
            data['request_location_message'] = await message.answer('Manzilni yuboring',
                                                                    reply_markup=request_location())


#
@dp.callback_query_handler(state=Checkout.location_check)
async def location_check(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await call.message.delete()
        await bot.delete_message(call.from_user.id, data['location_coordinates'].message_id)
        if call.data == 'verify_location':
            data['service_type'] = 3
            product = []
            for i in cart.get_cart(user_id=call.from_user.id):
                product.append({
                    'product_id': i.product_id,
                    'count': i.quantity
                })

                data['product'] = product.copy()
                data['cart_total'] = cart.cart_total(call.from_user.id)
            await bot.send_invoice(call.from_user.id,
                                   title='AFC Delivery',
                                   description='description',
                                   provider_token=PROVIDER_TOKEN,
                                   currency='UZS',
                                   need_phone_number=True,
                                   prices=[types.LabeledPrice(label="To'lovga", amount=data['cart_total'])],
                                   start_parameter='start_parameter',
                                   payload='test')

            await Checkout.payment.set()
        else:
            await Checkout.location.set()
            data['request_location_message'] = await call.message.answer('Manzilni yuboring',
                                                                         reply_markup=request_location())
