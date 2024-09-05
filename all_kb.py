from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from db import DataBase

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
SEE_SALARY = "Скока за месяц"
SEE_INCOME = "Скока седня"
OPEN = "Начать смену"
GET_MONTH_SALARY = "получить зп"
EXPENSES = "записать траты"

# CLOSE = "Закрыть смену"

master_buttons = [
    [KeyboardButton(text=SELL), KeyboardButton(text=SEE_BOOKS)],
    [KeyboardButton(text=SEE_SALARY), KeyboardButton(text=SEE_INCOME)],
    [KeyboardButton(text=OPEN), KeyboardButton(text=GET_MONTH_SALARY)],
    [KeyboardButton(text=EXPENSES)],
]

master_kb = ReplyKeyboardMarkup(keyboard=master_buttons, resize_keyboard=True)


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


def select_item_markup(items):
    return InlineKeyboardMarkup(
        inline_keyboard=items,
        resize_keyboard=True,
    )


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
