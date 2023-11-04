from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.database import DataBase

bot = Bot('TOKEN', parse_mode='HTML')

db = DataBase()

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

