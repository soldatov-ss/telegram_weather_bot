import logging
from typing import Union

import asyncpg
from asyncpg import Connection, UniqueViolationError
from asyncpg.pool import Pool

import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)  # - все записи списком
                elif fetchval:
                    result = await connection.fetchval(command, *args)  # - одна запись
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)  # - первая строка
                elif execute:
                    result = await connection.execute(command, *args)
                return result

    async def create_table_users(self):

        #  Таблица для хранение пользователей
        create_table_user = '''
        CREATE TABLE IF NOT EXISTS Users (
        user_id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        )
        '''

        # Таблица для хранения городов
        create_table_city = '''
        CREATE TABLE IF NOT EXISTS City (
        city_id SERIAL PRIMARY KEY,
        name_city VARCHAR(255) NOT NULL UNIQUE
        )
        '''

        # Таблица с отношением many to many
        create_table_user_cities = '''
        CREATE TABLE IF NOT EXISTS user_cities (
        user_id INT REFERENCES Users(user_id),
        city_id INT REFERENCES City(city_id),
        CONSTRAINT user_city_pkey PRIMARY KEY (user_id, city_id)
        )
        '''
        await self.execute(create_table_user, execute=True)
        await self.execute(create_table_city, execute=True)
        await self.execute(create_table_user_cities, execute=True)

    async def limit_3_cities(self, telegram_id):
        # Ограничение на пользователя - 3 города
        sql = f'''
            SELECT COUNT(*) FROM user_cities
            JOIN users USING(user_id)
            WHERE telegram_id = {telegram_id}
        '''
        count = await self.execute(sql, fetchval=True)
        return count

    async def select_users_city(self, telegram_id):

        sql = f'''
        SELECT City.name_city 
        FROM City
        JOIN user_cities USING (city_id)
        JOIN Users USING (user_id)
        WHERE Users.telegram_id = {telegram_id}
        '''
        result = await self.execute(sql, fetch=True)
        city_lst = [i.get('name_city') for i in result]
        return city_lst

    async def add_user(self, user: str, telegram_id: int):
        # Добавляет каждого нового пользователя в базу
        sql = f"INSERT INTO users(full_name, telegram_id) VALUES ('{user}', {telegram_id})"
        try:
            await self.execute(sql, execute=True)
        except UniqueViolationError:
            pass

    async def add_city(self, city: str, telegram_id: int):
        city = ' '.join(city).title()
        # Проверка на наличие города в табл
        sql = f"SELECT city_id FROM city WHERE  name_city = '{city}'"
        city_id = await self.execute(sql, fetchval=True)
        # Добавить новый город в табл и вернуть айди
        if not city_id:
            sql_two = f"INSERT INTO city(name_city) VALUES ('{city}') RETURNING city_id"
            city_id = await self.execute(sql_two, fetchval=True)

        # Добавить в табл many to many
        many_to_many = f'''
            INSERT INTO user_cities VALUES (
            (SELECT user_id FROM users WHERE telegram_id = {telegram_id}), {city_id})'''

        try:
            await self.execute(many_to_many, execute=True)
        except UniqueViolationError:
            return True  # вернуть, если уже есть этот город в табл many_to_many

    async def delete_city(self, city):
        # удалить город из табл many_to_many
        # city = ' '.join(city).title()
        sql = f'''
                DELETE FROM user_cities
                WHERE city_id = (SELECT city_id FROM city WHERE name_city = '{city}')
            '''
        await self.execute(sql, execute=True)

    async def select_all_users(self):
        # Для /all_users
        count = await self.execute('SELECT count(*) FROM Users', fetchval=True)
        return count

    async def select_all_cities(self):
        # Для /all_cities
        count = await self.execute('SELECT count(*) FROM city', fetchval=True)
        return count
