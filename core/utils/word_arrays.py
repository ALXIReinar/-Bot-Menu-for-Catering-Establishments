from datetime import datetime, timedelta

one_to_two = [
    'салаты',
    'супы',
    'горячие-блюда',
    'паста',
    'на-углях',
    'пицца',
    'десерты',
    'выпечка',
    'сезонное'
]

today = datetime.now().date()
week = today - timedelta(weeks=1)
month = today - timedelta(days=30)
year = today - timedelta(days=365)

definite_interval = 'SELECT date, "order", qtys FROM orders_history WHERE prsn_id = $1 AND date BETWEEN $2 AND $3 ORDER BY date ASC'

time_interval = {
    'неделя': (definite_interval, (week, today)),
    'месяц': (definite_interval, (month, today)),
    'год': (definite_interval, (year, today)),
}