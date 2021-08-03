import aiohttp
from aiogram import types
from aiogram.dispatcher.filters import CommandHelp, Command
from aiogram.types import CallbackQuery

import config
from keyboards import cite_keyboard, cities_keyboard, callback
from loader import dp, db
from utils.emoji import translate


@dp.message_handler(CommandHelp())
async def command_help(message: types.Message):
    text = ("<pre>Ты можешь добавлять и удалять в свой список города,",
            "которые ты хочешь отслеживать",
            "Также ты можешь посетить мой сайт</pre>",
            "Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/cities - Отслеживаемые города",
            "/add + <i>'название города'</i> - добавить город в список",
            "/delete + <i>'название города'</i> - удалить город из списка")
    await message.answer('\n'.join(text), reply_markup=cite_keyboard)


@dp.message_handler(Command('add'))
async def command_add(message: types.Message):
    count = await db.limit_3_cities(message.from_user.id)
    if count >= 3:
        text = '⛔\nК сожалению, у меня ограничение 😔\n' \
               'В твоем списке не может быть больше 3-х городов ☺\n' \
               '-------------------------\n' \
               'Если хочешь удалить лишний город - воспользуйся функцией 👇\n' \
               '/delete <i>название города</i>'
        return await message.reply(text)

    try:
        city = message.text.split()[1:]
    except IndexError:
        return await message.reply('<i>Чтобы добавить город попробуй так:\n'
                                   '/add название города</i>')

    if await db.add_city(city=city, telegram_id=message.from_user.id):
        return await message.reply('⛔ Этот город уже есть в твоем списке ⛔')

    await message.reply(f'Город добавлен! Осталось свободных ячеек: {2 - int(count)}')


@dp.message_handler(Command('delete'))
async def command_delete(message: types.Message):
    try:
        city = message.text.split()[1:]
    except IndexError:
        await message.reply('<i>Чтобы удалить город попробуй так:\n'
                            '/delete название города</i>')
        return

    city = ' '.join(city).title()
    user_cities = await db.select_users_city(telegram_id=message.from_user.id)

    if not city in user_cities:
        return await message.reply('⛔ Этого города нет в твоем списке ⛔\n'
                                   'Проверить список своих городов 👉 /cities')
    await db.delete_city(city)

    count = await db.limit_3_cities(message.from_user.id)
    await message.reply(f'Город был удален из списка! Осталось свободных ячеек: {3 - int(count)}')


@dp.message_handler(Command('cities'))
async def command_cities(message: types.Message):
    cities = await db.select_users_city(message.from_user.id)
    await message.answer('Твои города: \n{}'.format("\n".join(cities)), reply_markup=cities_keyboard)


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


@dp.callback_query_handler(callback.filter(data='weather_in'))
async def callback_weather_in_cities(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    cities = await db.select_users_city(call.from_user.id)
    for city in cities:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.APPID}&units=metric'
        response = await get(url)
        try:
            description = response['weather'][0]['main']  # ловим ошибку на неправильное название города
        except KeyError:
            continue
        description_on_russian, emoji = translate(description)

        answer = f'''
                Город: <b>{city.title()}</b>
                Описание: {emoji} {description_on_russian} {emoji}
                Температура: {response['main']['temp']} °C
                Скорость ветра: {response['wind']['speed']} м/с
            '''
        await call.message.answer(answer)
