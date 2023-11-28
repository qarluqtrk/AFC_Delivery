from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import PROVIDER_TOKEN, ADMINS
from handlers.users.start import bot_start
from keyboards.default.key import request_phone_number, request_location
from keyboards.inline.cart import cart_keyboard
from keyboards.inline.ordering import select_type_of_service, verify_location
from keyboards.inline.start import start_keyboard
from loader import dp, afc, cart, bot
from states.menu import Checkout
from utils.db_api.afcData import session, Cart
from utils.geo_py import get_location


# cart view

@dp.callback_query_handler(text="cart")
async def cart_view(call: types.CallbackQuery):
    if not cart.check(user_id=call.from_user.id):
        await call.message.edit_caption("Savatingiz bo'sh", reply_markup=start_keyboard(call.from_user.id))
    else:
        try:
            loading = await call.message.edit_caption("Savatingiz yuklanmoqda...")
            await call.message.answer(f"To'lovga {cart.cart_total(call.from_user.id)[:-2]} so'm berildi\n"
                                      "Quyida sizning savatingiz: ",
                                      reply_markup=cart_keyboard(user_id=call.from_user.id))
            await loading.delete()
            await Checkout.cart.set()
        except:
            cart.clear(user_id=call.from_user.id)
            await call.message.edit_caption("Savatingiz bo'sh", reply_markup=start_keyboard(call.from_user.id))


@dp.callback_query_handler(state=Checkout.cart)
async def cart_handler(call: types.CallbackQuery, state):
    if call.data.startswith('plus'):
        cart_item_id = call.data.split(' - ')[1]
        cart_item = session.query(Cart).filter(Cart.id == cart_item_id).first()
        cart_item.quantity += 1
        session.commit()
        await call.message.edit_text(text=f"To'lovga {cart.cart_total(call.from_user.id)[:-2]} so'm berildi\n"
                                          "Quyida sizning savatingiz: ",
                                     reply_markup=cart_keyboard(user_id=call.from_user.id))
    elif call.data.startswith('minus'):
        cart_item_id = call.data.split(' - ')[1]
        cart_item = session.query(Cart).filter(Cart.id == cart_item_id).first()
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            session.commit()
            await call.message.edit_text(
                text=f"To'lovga {cart.cart_total(call.from_user.id)[:-2]} so'm berildi\n"
                     "Quyida sizning savatingiz: ", reply_markup=cart_keyboard(user_id=call.from_user.id))
    elif call.data.startswith("delete"):
        cart_item_id = call.data.split(' - ')[1]
        session.query(Cart).filter(Cart.id == cart_item_id).delete()
        session.commit()
        if cart.check(user_id=call.from_user.id):
            await call.message.edit_text(text=f"To'lovga {cart.cart_total(call.from_user.id)[:-2]} so'm berildi\n"
                                              "Quyida sizning savatingiz: ",
                                         reply_markup=cart_keyboard(user_id=call.from_user.id))
        else:
            await call.message.answer("Savatingiz tozalandi")
            await call.message.delete()
            await state.finish()
            await bot_start(call.message)
    elif call.data == 'back_to_main':
        photo_path = 'images/afc-logo.png'
        with open(photo_path, 'rb') as photo:
            await call.message.answer_photo(
                photo=photo,
                caption="Assalomu Alaykum!\n"
                        "AFC ga xush kelibsiz!\n"
                        "Sizni menyu bilan tanishtirishim, buyurtma olishim va joy band qilishingizga yordam berishim mumkin\n"
                        "Davom etish uchun quyidagi tugmalardan birini bosing👇👇",
                reply_markup=start_keyboard(user_id=call.from_user.id))
        await call.message.delete()
        await state.finish()
    elif call.data == 'clear_cart':
        session.query(Cart).filter(Cart.user_id == call.from_user.id).delete()
        session.commit()
        await call.message.answer("Savatingiz tozalandi")
        await call.message.delete()
        await state.finish()
        await bot_start(call.message)
    else:
        await call.message.edit_text('Buyurtma turini tanlang', reply_markup=select_type_of_service())
        await Checkout.service_type.set()


