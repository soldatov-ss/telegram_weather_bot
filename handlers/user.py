import aiohttp
from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.exceptions import BadRequest

import config
from keyboards import keyboard
from loader import dp, db
from utils import rate_limit
from utils.emoji import translate

@rate_limit(limit=5)
@dp.message_handler(CommandStart())
async def start_app(message: types.Message):
    await db.add_user(message.from_user.full_name, message.from_user.id)
    text = '\n'.join([f'Привет {message.from_user.full_name}!',
                      f'☀ Я смогу подсказать погоду в любом городе! ☀',
                      f'Передай мне свою геолокацию нажав на кнопку ниже',
                      f'Либо просто напиши мне название твоего города'])

    try:
        # Ловим ошибку если юзер нажал старт в канале, а не в боте
        await message.answer(text, reply_markup=keyboard)
    except BadRequest:
        text = '\n'.join([f'Привет {message.from_user.full_name}!',
                          f'☀ Я смогу подсказать погоду в любом городе! ☀',
                          f'Напиши мне название твоего города 😏'])
        await message.answer(text)


async def get(url):
    # Асинхронный запрос по урлу
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

@rate_limit(limit=3)
@dp.message_handler()
async def weather_city(message: types.Message):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={config.APPID}&units=metric'

    response = await get(url)
    try:
        description = response['weather'][0]['main']
    except KeyError:
        await message.answer('Такого города нет в моем списке😔 \nПопробуй еще раз!😊')
        return

    description_on_russian, emoji = translate(description)

    answer = f'''
        Город: {message.text.title()}, 
        \nОписание: {emoji} {description_on_russian} {emoji},
        \nТемпература: {response['main']['temp']} °C,
        \nСкорость ветра: {response['wind']['speed']} м/с
    '''
    await message.answer(answer)


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def get_location(message: types.Message):
    location = message.location
    lat = location.latitude
    lon = location.longitude
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={config.APPID}&units=metric'
    response = await get(url)
    description = response['weather'][0]['main']
    description_on_russian, emoji = translate(description)

    answer = f'''
        Город: {response['name']}
        \nОписание: {emoji} {description_on_russian} {emoji}
        \nТемпература: {response['main']['temp']} °C
        \nСкорость ветра: {response['wind']['speed']} м/с
    '''
    await message.answer(answer)
