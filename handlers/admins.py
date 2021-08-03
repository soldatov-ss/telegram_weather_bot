from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, db


@dp.message_handler(Command('all_users'))
async def count_users(message: types.Message):
    count = await db.select_all_users()
    await message.answer(f'Всего в базе пользователей: {count}')


@dp.message_handler(Command('all_cities'))
async def count_users(message: types.Message):
    count = await db.select_all_cities()
    await message.answer(f'Всего в базе городов: {count}')
