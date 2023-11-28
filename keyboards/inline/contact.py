from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def contact():
    keyboard = InlineKeyboardMarkup(row_width=2)

    # Define buttons
    instagram_button = InlineKeyboardButton("📸Instagram", url='https://www.instagram.com/p/CzOL3A5t9gA/')
    tiktok_button = InlineKeyboardButton("📱TikTok", url='http://www.tiktok.com/@afc_food')
    website_button = InlineKeyboardButton("💻Website", url='https://www.afc-foods.uz/')
    location_button = InlineKeyboardButton("📍Manzil", url='https://goo.gl/maps/6qWwY5HtJYhJxHrC8')
    back_button = InlineKeyboardButton("⬅️Orqaga", callback_data='back')

    # Add buttons to the keyboard
    keyboard.add(website_button)
    keyboard.add(instagram_button, tiktok_button)
    keyboard.add(location_button)
    keyboard.add(back_button)
    return keyboard
