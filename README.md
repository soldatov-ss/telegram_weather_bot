Телеграм бот с базой данных Postrgesql, который позволяет отслеживать текую погоду в любом городе

В данный момент бот загружен на сервер AWS

Никнейм бота: **@soldatov_test_bot**

Возможности: 
-----------
- добавлять/удалять 3 города в свой список для отслеживания погоды (сделано только 3(можно увеличить) чтобы не было много мусора в телеграме и частых запросов);
- эхо хендлер ловит все сообщения, т.е. можно передать название города и бот тебе пришлет текущую погоду в городе;
- передача своей геопозиции, чтобы уточнить погоду по своей местности, с помощью текстовой кнопки;
- инлайн кнопка, с помощью которой отобразится погода в всех городах твоего списка;
- две админ команды, для уточнения кол-ва городов и кол-ва людей запустивших бота;
- тротлинг мидлварь, чтобы не было спама и частых запросов на API.


Список команд:
------------
- /add название города - добавить город в твой список;
- /delete название города - удалить город из твоего списка;
- /help - выведет справку по боту и командам;
- /cities - выведет все твои города в списке и инлайн кнопку;
- /start - запускает бота и добавляет пользователя в базу.
----------
Админ комманды
----------
- /all_users - покажет кол-во пользователей, которые запускали бота;
- /all_cities - покажет кол-во всех городов, которые были добавлены в базу.
