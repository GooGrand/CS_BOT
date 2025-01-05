from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from db import DataBase
from datetime import datetime, timedelta

db = DataBase()

confirm_buttons = [
    [KeyboardButton(text="Подтвердить"), KeyboardButton(text="Начать сначала")]
]

confirm_kb = ReplyKeyboardMarkup(keyboard=confirm_buttons, resize_keyboard=True)

start_buttons = [
    [
        KeyboardButton(text="Забронировать столик"),
        KeyboardButton(text="Мои бронирования"),
        # KeyboardButton(text="Написать кальянному мастеру"),
        KeyboardButton(text="Написать кальянному мастеру"),
        # KeyboardButton(text="отправить контакт", request_contact=True),
    ]
]

start_kb = ReplyKeyboardMarkup(keyboard=start_buttons, resize_keyboard=True)

SELL = "Замутить продажу"
SEE_BOOKS = "Посмотреть брони"
DISCOUNTERS = "Господа пидарасы"
STATS = "Статистика"
OPEN = "Начать смену"

EXPENSES = "записать траты"

GET_MONTH_SALARY = "Подглядеть зп"
ITEMS_TODAY = "Продажи сегодня"
SEE_INCOME = "Скока седня"
BACK = "Назад"
# CLOSE = "Закрыть смену"

master_buttons = [
    [KeyboardButton(text=SELL), KeyboardButton(text=SEE_BOOKS), KeyboardButton(text=DISCOUNTERS)],
    [KeyboardButton(text=STATS), KeyboardButton(text=OPEN), KeyboardButton(text=EXPENSES),],
]

master_kb = ReplyKeyboardMarkup(keyboard=master_buttons, resize_keyboard=True)

stats_buttons = [
    [
        KeyboardButton(text=GET_MONTH_SALARY),
        KeyboardButton(text=ITEMS_TODAY),
    ],
    [KeyboardButton(text=BACK), KeyboardButton(text=SEE_INCOME)],
]

stats_kb = ReplyKeyboardMarkup(keyboard=stats_buttons, resize_keyboard=True)


class ItemCallback(CallbackData, prefix="item"):
    item_id: int


def select_item_buttons():
    items = db.get_items()
    all_items = [
        InlineKeyboardButton(
            text=data[1], callback_data=ItemCallback(item_id=data[0]).pack()
        )
        for data in items
    ]
    return [
        all_items[i * 2 : (i + 1) * 2] for i in range((len(all_items) + 2 - 1) // 2)
    ]


def create_markup(items):
    return InlineKeyboardMarkup(
        inline_keyboard=items,
        resize_keyboard=True,
    )

class DiscountCallback(CallbackData, prefix="discount"):
    item_id: int

def discount_buttons():
    discounters = db.get_discounters()
    all_items = [
        InlineKeyboardButton(
            text=data[1], callback_data=ItemCallback(item_id=data[0]).pack()
        )
        for data in items
    ]
    return [
        all_items[i * 2 : (i + 1) * 2] for i in range((len(all_items) + 2 - 1) // 2)
    ]



class PaymentCallback(CallbackData, prefix="payment"):
    payment_type: str


payment_buttons = [
    [
        InlineKeyboardButton(
            text="Кеш", callback_data=PaymentCallback(payment_type="cash").pack()
        ),
        InlineKeyboardButton(
            text="Перевод",
            callback_data=PaymentCallback(payment_type="transfer").pack(),
        ),
    ]
]


payment_kb = InlineKeyboardMarkup(inline_keyboard=payment_buttons, resize_keyboard=True)


class ExpensesCallback(CallbackData, prefix="expense"):
    expense_type: str


expense_buttons = [
    [
        InlineKeyboardButton(
            text="Табак", callback_data=ExpensesCallback(expense_type="tobacco").pack()
        ),
        InlineKeyboardButton(
            text="Уголь",
            callback_data=ExpensesCallback(expense_type="coal").pack(),
        ),
    ],
    [
        InlineKeyboardButton(
            text="напитки",
            callback_data=ExpensesCallback(expense_type="drinks").pack(),
        ),
        InlineKeyboardButton(
            text="Аренда",
            callback_data=ExpensesCallback(expense_type="rent").pack(),
        ),
    ],
    [
        InlineKeyboardButton(
            text="Зарплата",
            callback_data=ExpensesCallback(expense_type="salary").pack(),
        ),
        InlineKeyboardButton(
            text="Другое",
            callback_data=ExpensesCallback(expense_type="other").pack(),
        ),
    ],
]


expense_kb = InlineKeyboardMarkup(inline_keyboard=expense_buttons, resize_keyboard=True)


get_phone_button = [
    [
        KeyboardButton(text="Отправить номер телефона", request_contact=True),
    ]
]


get_phone_kb = ReplyKeyboardMarkup(
    keyboard=get_phone_button, resize_keyboard=True, one_time_keyboard=True
)

date_buttons = [
    [
        InlineKeyboardButton(text="Понедельник", callback_data="date"),
        InlineKeyboardButton(text="Вторник", callback_data="date"),
        InlineKeyboardButton(text="Среда", callback_data="date"),
        InlineKeyboardButton(text="Четверг", callback_data="date"),
        InlineKeyboardButton(text="Пятница", callback_data="date"),
        InlineKeyboardButton(text="Суббота", callback_data="date"),
        InlineKeyboardButton(text="Воскресенье", callback_data="date"),
    ],
]
date_kb = InlineKeyboardMarkup(inline_keyboard=date_buttons)

days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вск"]


def get_date_kb():
    today = datetime.now()
    start_of_week = today
    dates_this_week = []
    for i in range(7):
        date = start_of_week + timedelta(days=i)
        dates_this_week.append(date)

    date_buttons = [
        [
            InlineKeyboardButton(
                text=f"{days_of_week[dates_this_week[0].weekday()]}({dates_this_week[0].strftime('%m-%d')})",
                callback_data="date",
            ),
            InlineKeyboardButton(
                text=f"{days_of_week[dates_this_week[1].weekday()]}({dates_this_week[1].strftime('%m-%d')})",
                callback_data="date",
            ),
            InlineKeyboardButton(
                text=f"{days_of_week[dates_this_week[2].weekday()]}({dates_this_week[2].strftime('%m-%d')})",
                callback_data="date",
            ),
            InlineKeyboardButton(
                text=f"{days_of_week[dates_this_week[3].weekday()]}({dates_this_week[3].strftime('%m-%d')})",
                callback_data="date",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{days_of_week[dates_this_week[4].weekday()]}({dates_this_week[4].strftime('%m-%d')})",
                callback_data="date",
            ),
            InlineKeyboardButton(
                text=f"{days_of_week[dates_this_week[5].weekday()]}({dates_this_week[5].strftime('%m-%d')})",
                callback_data="date",
            ),
            InlineKeyboardButton(
                text=f"{days_of_week[dates_this_week[6].weekday()]}({dates_this_week[6].strftime('%m-%d')})",
                callback_data="date",
            ),
        ],
    ]
    date_kb = InlineKeyboardMarkup(inline_keyboard=date_buttons)
    return date_kb
