from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.start import start_keyboard
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    photo_path = 'images/afc-logo.png'
    with open(photo_path, 'rb') as photo:
        await message.answer_photo(
            photo=photo,
            caption="Assalomu Alaykum!\n"
                    "AFC ga xush kelibsiz!\n"
                    "Sizni menyu bilan tanishtirishim, buyurtma olishim va joy band qilishingizga yordam berishim mumkin\n"
                    "Davom etish uchun quyidagi tugmalardan birini bosing👇👇",
            reply_markup=start_keyboard(user_id=message.from_user.id))


@dp.message_handler(CommandStart(), state='*')
async def bot_start_state(message: types.Message, state: FSMContext):
    photo_path = 'images/afc-logo.png'
    with open(photo_path, 'rb') as photo:
        await message.answer_photo(
            photo=photo,
            caption="Assalomu Alaykum!\n"
                    "AFC ga xush kelibsiz!\n"
                    "Sizni menyu bilan tanishtirishim, buyurtma olishim va joy band qilishingizga yordam berishim mumkin\n"
                    "Davom etish uchun quyidagi tugmalardan birini bosing👇👇",
            reply_markup=start_keyboard(user_id=message.from_user.id))
        await state.finish()
