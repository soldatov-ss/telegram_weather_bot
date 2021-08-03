from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


callback = CallbackData('city', 'data')

cite_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Сайт',
                url='https://soldatov-weather-app.herokuapp.com/'
            )
        ]
    ])

cities_keyboard = InlineKeyboardMarkup(row_width=2,
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(
                                                   text='Погода в городах',
                                                   callback_data=callback.new(data='weather_in')
                                               )
                                           ]
                                       ]
                                       )
