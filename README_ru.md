# 🧁Бот-Меню для Ресторанов и Кафе

![Python ver](https://img.shields.io/badge/pyhon-3.10-orange)
![aiogram](https://img.shields.io/badge/aiogram-3.13.1-blue)
![arq](https://img.shields.io/badge/arq-0.26.1-yellow)
![elasticsearch](https://img.shields.io/badge/elasticsearch-8.15.4-green)
![postgres](https://img.shields.io/badge/postgre-16-42a4ff)
![redis](https://img.shields.io/badge/redis-5.2.0-red)

## 🧩 Таблицы БД 

> core > config_main > pg_settings.py

#### Представлены полные схемы таблиц. Были составлены через PgAdmin4, поэтому не могу быть уверен за работоспосбность кода таблиц

> core > data > posgre.py > PgSql

#### Там представлены столбцы и таблицы, в которых они представлены, в более кратком виде

## 📝 Основная идея

Бот, выполняющий роль ```ресторанного меню```, с возможностью ```поиска блюд```

#### Приём «**Ёлочка**»🌲 (Бинарный поиск)
* 1. Посетитель перемещается по группам блюд
* 2. Добавляет желаемые блюда в заказ
* 3. Открывает собранный заказ
#### 🔎Поиск с помощью Elasticsearch
* 1. Посетитель вводит поисковой запрос
* 2. Происходит релевантная выдача результатов, поделённых на группы

## Меню 🍽

#### Выбор блюда разбит на 2-3 группы. Комманда `/menu` 

![1lvl](https://sun9-33.userapi.com/impg/MwjDb8iSoMrVmNNL9wRqXt7JUr0c_UIurLlC5w/urvx8tNRKP8.jpg?size=1223x243&quality=95&sign=5110a58085f9c1369838a412163b9576&type=album)


### Если выбирают «Роллы🍱» или «Закуски🥪»
![2lvl](https://sun36-2.userapi.com/impg/COahWfHPVD0OvUsfvx9EtmWjQ4CRp2_VDZTzUA/YuTL16RQn7w.jpg?size=1221x118&quality=95&sign=e6ad87b5f959b075bb731b7a9bfd6a24&type=album)

### Выдача 🛄
![extradition](https://sun9-35.userapi.com/impg/JPnQBKcY7FS8KPmPOo3w1U0gHeYPTEiKGC_09g/xcsbduhng5I.jpg?size=689x867&quality=95&sign=615aa6940440a69e7ba6e7ae92aa4cca&type=album)

## 🎲 Взаимодействие с блюдами 

#### Ты можешь ```добавить``` его ```в корзину```, после чего выбрать ```количество блюд('+', '-')``` 
![CRD(shorted CRUD)](introduction_intrctn.gif)

#### Всё, что ты добавишь в заказ, можно посмотреть по команде ```/my_order```
![order](https://sun9-37.userapi.com/impg/N5gXPgHYbMvjFuVRParxS2Em552lLytcZO6H6Q/-Rty5_3AyEg.jpg?size=598x237&quality=95&sign=1f15b7cb5724763a720e8dbaa8bbc4ce&type=album)

## ⏱️ Задача arq в проекте

> core > menu > menu_3lvl.py > arq_run()

1. Весь заказ находится в редисе в соображениях производительности
2. Заказ переносится в БД в конце рабочего дня заведения, когда посетители уже ушли⏰

Это и быстро, и заказ всегда достпуен. БД не нагружается постоянными АПДЕЙТ-запросами

```python
hour, minute, second = now.hour - 2, now.minute, now.second
now_in_seconds = 3600 * hour + 60 * minute + second

ttl = day - now_in_seconds
await redis.set(f'_{chat_id}', data)
await arq.enqueue_job('redis_save_n_flush',
                      _defer_by=timedelta(seconds=ttl-300),
                      chat_id=chat_id)
```

## История заказов

> core > orders_history.py

#### Просто сохранённые заказы, выдаваемые с различными временными ограничениями🕘. Команда `/orders_history`
![orders history](https://sun9-9.userapi.com/impg/mdXOOuaT5h29WEaH1iWnxRmO5akWcDhEf-AzJA/SBV0DH38zks.jpg?size=466x470&quality=95&sign=1ad3d1bef994f40fcee9d11b7a193937&type=album) 

## 🔎 Поиск

> core > searching

#### По запросу пользователя группами выдаются документы📘 из Elasticsearch, с подходящими данными. Поиск ведётся по Названию и Описанию. Маппинг индекса🧶 расположен по пути `> core > config_main > index_settings.py`

#### Поисковой паттерн находится в `./search_pattern.py`

#### Команда `/search`
![searching](https://sun9-52.userapi.com/impg/5pqCJLSDLN_sPjLKZjW2iw-PChimtSnKFzdzdQ/Rk2wVUIdhEA.jpg?size=603x740&quality=95&sign=0819d4a3183e5c5016bd3031d9541b33&type=album)

## Спасибо за прочтение! ✨😇
