from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from data.config import PROVIDER_TOKEN
from keyboards.default.key import request_location
from keyboards.inline.cart import cart_keyboard
from keyboards.inline.start import start_keyboard
from loader import dp, bot, cart, afc
from states.menu import Checkout


@dp.callback_query_handler(state=Checkout.service_type)
async def service_type_view(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        product = []
        cart_items = cart.get_cart(user_id=call.from_user.id)

        poster_products = afc.get_products()
        products = {}
        for i in poster_products:
            products[i['product_id']] = i

    for cart_item in cart_items:
        if cart_item.modificator_id is None:
            product.append(

                {
                    'product_id': cart_item.product_id,
                    'count': cart_item.quantity
                }

            )
        else:
            t = products[cart_item.product_id]
            print("")
            if 'modifications' in t:
                product.append({
                    'product_id': cart_item.product_id,
                    "modificator_id": cart_item.modificator_id,
                    'count': cart_item.quantity

                })

            elif "group_modifications" in t:
                product.append({
                    'product_id': cart_item.product_id,
                    "modifications": [{"m": cart_item.modificator_id, "a": 1}],
                    'count': cart_item.quantity
                })

        data['product'] = product.copy()
        data['cart_total'] = cart.cart_total(call.from_user.id)
        if call.data == 'delivery':
            data['service_type'] = 3
            data['request_location_message'] = await call.message.answer('Manzilni yuboring',
                                                                         reply_markup=request_location())
            await call.message.answer(text='Manzilni yuboring',
                                      reply_markup=ReplyKeyboardRemove())
            await call.message.delete()
            await Checkout.location.set()
        elif call.data == 'takeout':
            data['service_type'] = 2
            await Checkout.payment.set()

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
            if not cart.check(user_id=call.from_user.id):
                await call.message.answer("Savatingiz bo'sh", reply_markup=start_keyboard(call.from_user.id))
            else:
                try:
                    loading = await call.message.answer("Savatingiz yuklanmoqda...")
                    await call.message.answer(f"To'lovga {cart.cart_total(call.from_user.id)[:-2]} so'm berildi\n"
                                              "Quyida sizning savatingiz: ",
                                              reply_markup=cart_keyboard(user_id=call.from_user.id))
                    await loading.delete()
                    await Checkout.cart.set()
                except:
                    cart.clear(user_id=call.from_user.id)
                    await call.message.answer("Savatingiz bo'sh", reply_markup=start_keyboard(call.from_user.id))
            await call.message.delete()


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
                await message.answer("Buyurtma jo'natildi")
        else:
            a = afc.create_delivery_order(phone=data['phone_number'],
                                          first_name=data['name'],
                                          payment=data['payment'],
                                          products=data['product'],
                                          service_type=3,
                                          client_address=data['location'])
            if a:
                await message.answer("Buyurtma jo'natildi")

        # Clear cart
        cart.clear(user_id=message.from_user.id)
        with open("images/afc-logo.png", "rb") as photo:
            await message.answer_photo(photo=photo, caption="Savatingiz tozalandi",
                                       reply_markup=start_keyboard(message.from_user.id))
            await state.finish()
