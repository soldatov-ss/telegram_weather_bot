from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")
APPID = env.str("APPID")  # токен с сайта с погодой https://openweathermap.org/api

DB_USER = env.str('DB_USER')
DB_PASS = env.str('DB_PASS')
DB_NAME = env.str('DB_NAME')
DB_HOST = env.str('DB_HOST')
