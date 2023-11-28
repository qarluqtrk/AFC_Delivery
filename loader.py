from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from data.config import POSTER_API
from utils.db_api.afcData import Cart
from utils.poster_api.AFC import PosterAPI

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
cart = Cart()

afc = PosterAPI(POSTER_API)
