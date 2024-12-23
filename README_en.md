# 🧁Bot-Menu for Catering Establishments

![Python ver](https://img.shields.io/badge/pyhon-3.10-orange)
![aiogram](https://img.shields.io/badge/aiogram-3.13.1-blue)
![arq](https://img.shields.io/badge/arq-0.26.1-yellow)
![elasticsearch](https://img.shields.io/badge/elasticsearch-8.15.4-green)
![postgres](https://img.shields.io/badge/postgre-16-42a4ff)
![redis](https://img.shields.io/badge/redis-5.2.0-red)

## 🧩 DB shemas

> core > config_main > pg_settings.py

#### Complete table diagrams are presented. They were compiled via pgAdmin4, so I can't be sure of the workability of the tables' code.

> core > data > posgre.py > PgSql

#### The columns and tables in which they are presented are presented there in a more concise form.

## 📝 Project Model Основная идея

A Bot that performs the functions of a ```restaurant menu```, with the ability to ```search for dishes```

#### Reception «**Herringbone**»🌲 (Binary search)
* 1. The visitor moves through groups of dishes
* 2. Adds desired dishes to the order
* 3. Opens the collected order

#### 🔎Search by Elasticsearch
* 1. The visitor types a search query
* 2. There is a relevant output of results divided into groups

## Menu 🍽

> core > menu 

### The choice of dishes is divided into 2-3 groups. Command `/menu`

![1lvl](https://sun9-33.userapi.com/impg/MwjDb8iSoMrVmNNL9wRqXt7JUr0c_UIurLlC5w/urvx8tNRKP8.jpg?size=1223x243&quality=95&sign=5110a58085f9c1369838a412163b9576&type=album)


### If you choose «Роллы🍱» or «Закуски🥪»
![2lvl](https://sun36-2.userapi.com/impg/COahWfHPVD0OvUsfvx9EtmWjQ4CRp2_VDZTzUA/YuTL16RQn7w.jpg?size=1221x118&quality=95&sign=e6ad87b5f959b075bb731b7a9bfd6a24&type=album)

### Extradition 🛄
![extradition](https://sun9-35.userapi.com/impg/JPnQBKcY7FS8KPmPOo3w1U0gHeYPTEiKGC_09g/xcsbduhng5I.jpg?size=689x867&quality=95&sign=615aa6940440a69e7ba6e7ae92aa4cca&type=album)

## 🎲 Interaction with dishes

> core > main_order

#### You can ``add`` it ```to the basket``` and then select ```number of dishes('+', '-')```
![CRD(shorted CRUD)](introduction_intrctn.gif)

#### Everything that you add to the order can be viewed using the command `/my_order`
![order](https://sun9-37.userapi.com/impg/N5gXPgHYbMvjFuVRParxS2Em552lLytcZO6H6Q/-Rty5_3AyEg.jpg?size=598x237&quality=95&sign=1f15b7cb5724763a720e8dbaa8bbc4ce&type=album)

## ⏱️ The arq task in the project

> core > menu > menu_3lvl.py > arq_run()

1. The entire order is in Redis in performance considerations
2. The order is transferred to the database at the end of the business day of the establishment, when the visitors have already left⏰

It's fast, and the order is always available. The DB is not loaded with constant UPDATE queries🌀

```python
hour, minute, second = now.hour - 2, now.minute, now.second
now_in_seconds = 3600 * hour + 60 * minute + second

ttl = day - now_in_seconds
await redis.set(f'_{chat_id}', data)
await arq.enqueue_job('redis_save_n_flush',
                      _defer_by=timedelta(seconds=ttl-300),
                      chat_id=chat_id)
```

## 📃 Orders History

> core > orders_history.py

#### Just saved orders issued with different time constraints🕘. The `/order_history` command
![orders history](https://sun9-9.userapi.com/impg/mdXOOuaT5h29WEaH1iWnxRmO5akWcDhEf-AzJA/SBV0DH38zks.jpg?size=466x470&quality=95&sign=1ad3d1bef994f40fcee9d11b7a193937&type=album)

## 🔎 Searching

> core > searching

#### At the request of the user, the groups are issued documents📘 with the appropriate data from Elasticsearch. The search is based on the Name and Description. The index🧶 mapping is located along the path `> core > config_main > index_settings.py`

#### The search pattern is located in `./search_pattern.py`

#### Command `/search`
![searching](https://sun9-52.userapi.com/impg/5pqCJLSDLN_sPjLKZjW2iw-PChimtSnKFzdzdQ/Rk2wVUIdhEA.jpg?size=603x740&quality=95&sign=0819d4a3183e5c5016bd3031d9541b33&type=album)


## Thanks for Reading✨😇
