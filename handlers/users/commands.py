from data.loader import bot, dp, db
from aiogram.types import Message
from .text_handlers import start_language, show_main_menu
from aiogram.dispatcher import FSMContext
from states.states import NumberState

@dp.message_handler(commands=['start'], state='*')
async def command_start(message: Message, state: FSMContext):
    await state.finish()
    user = db.get_user_by_id(message.chat.id)
    if user:
        '''Показать главное меню'''
        await show_main_menu(message)
    else:
        await start_language(message)
    # Регестрация по номеру телефона

@dp.message_handler(commands=['menu'])
async def command_menu(message: Message):
    await message.answer('https://telegra.ph/Nashe-menyu-06-03-11')

@dp.message_handler(commands=['feedback'])
async def command_feedback(message: Message):
    await message.answer('<b>Единый call-center:</b> +998(88) 005-55-35 или +998(88) 123-21-23')