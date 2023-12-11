from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def contact():
    keyboard = InlineKeyboardMarkup(row_width=2)

    # Define buttons
    instagram_button = InlineKeyboardButton("📸Instagram", url='https://www.instagram.com/p/CzOL3A5t9gA/')
    tiktok_button = InlineKeyboardButton("📱TikTok", url='http://www.tiktok.com/@afc_food')
    website_button = InlineKeyboardButton("💻Website", url='https://www.afc-foods.uz/')
    location_button = InlineKeyboardButton("📍Manzil", url='https://www.google.com/maps/place/Clever+qarshi/@38.8368838,65.779254,17z/data=!3m1!4b1!4m6!3m5!1s0x3f4ea98e1091f4e3:0x14ffce588cd416b9!8m2!3d38.8368838!4d65.7818289!16s%2Fg%2F11r_np7yzk?entry=ttu')
    back_button = InlineKeyboardButton("⬅️Orqaga", callback_data='back')

    # Add buttons to the keyboard
    keyboard.add(website_button)
    keyboard.add(instagram_button, tiktok_button)
    keyboard.add(location_button)
    keyboard.add(back_button)
    return keyboard
