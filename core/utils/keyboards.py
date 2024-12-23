from datetime import datetime
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardBuilder


def menu_branch_1lvl():
    def season():
        current_month = datetime.now().month
        autumn = current_month in range(9,12)
        spring = current_month in range(3,6)
        summer = current_month in range(6,9)

        year_time = '❄️'
        if autumn:
            year_time = '🍁'
        elif spring:
            year_time = '🌿'
        elif summer:
            year_time = '☀️'
        return year_time

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='Закуски🥪'), KeyboardButton(text='Салаты🥗'), KeyboardButton(text='Супы🍜')
        ],
        [
            KeyboardButton(text='Горячие блюда🥘'), KeyboardButton(text='Паста🍝'), KeyboardButton(text='На углях🔥')
        ],
        [
            KeyboardButton(text='Роллы🍱'), KeyboardButton(text='Пицца🍕'), KeyboardButton(text='Десерты🍧')
        ],
        [
            KeyboardButton(text='Выпечка🥐'), KeyboardButton(text=f'Сезонное{season()}')
        ]
    ])
    return markup

def Cold_Hot():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='Холодные🧊'), KeyboardButton(text='Горячие📛')
        ],
        [
            KeyboardButton(text='Назад⬆️')
        ]
    ])
    return markup


def add_basket(id):
    call_data = f'*_{id}_1'

    markup = InlineKeyboardBuilder()
    markup.button(text='Добавить к заказу🛒', callback_data=call_data)
    markup.adjust(1)
    return markup.as_markup()

def rm_basket(id, n=1):
    call_data = f'/_{id}_{n}'

    markup = InlineKeyboardBuilder()
    markup.button(text='Исключить❌', callback_data=call_data)
    markup.button(text=str(n), callback_data='counter')
    markup.button(text='-', callback_data=f'rm_{id}_{n}')
    markup.button(text='+', callback_data=f'add_{id}_{n}')
    markup.adjust(1, 3)
    return markup.as_markup()

def add_smth():
    markup = InlineKeyboardBuilder()

    markup.button(text='Добавить ещё➕', callback_data='more')
    markup.adjust(1)
    return markup.as_markup()

def user_by_id(id):
    link = f'tg://user?id={id}'
    markup = InlineKeyboardBuilder()

    markup.button(text='Инициатор', url=link)
    markup.adjust(1)
    return markup.as_markup()

def time_intervals():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='Неделя'), KeyboardButton(text='Месяц'),
            KeyboardButton(text='Год'), KeyboardButton(text='За Всё Время')
        ],
        [
            KeyboardButton(text='Указать дату')
        ]
    ])
    return markup

def get_more(value: int):
    call_data = 'thats_all!'
    if value:
        call_data = 'search_residue'

    markup = InlineKeyboardBuilder()
    markup.button(text=f'Показать больше    +{value}', callback_data=call_data)
    return markup.as_markup()

def cancel():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Что случилось?", keyboard=[
        [
            KeyboardButton(text="Отмена🚫")
        ]
    ])
    return markup

def tech_sup_kb(id_appeal: int):
    markup = InlineKeyboardBuilder()

    markup.button(text='Прочитано🟢', callback_data='read-it')
    markup.button(text='Ответить🖌', callback_data=f'reply-to_{id_appeal}')
    markup.button(text='Мусор!🔴', callback_data=f'trash_{id_appeal}')
    markup.adjust(1,1,1)

    return markup.as_markup()
