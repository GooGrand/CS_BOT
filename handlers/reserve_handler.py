from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import types
from state_list import reserve_form
from all_kb import confirm_kb, start_kb, get_phone_kb, get_date_kb, DateCallback
from db import DataBase
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import Command
from main import bot
from datetime import datetime


router = Router()

db = DataBase()


# @router.message(F.text.lower() == "календарь")
# async def dialog_cal_handler(message: Message):
#     await message.answer(
#         "Please select a date: ",
#         reply_markup=await DialogCalendar(
#             locale=await get_user_locale(message.from_user)
#         ).start_calendar(year=2024, month=9),
#     )


# @router.callback_query(DialogCalendarCallback.filter())
# async def process_dialog_calendar(
#     callback_query: CallbackQuery, callback_data: CallbackData
# ):
#     selected, date = await DialogCalendar(
#         locale=await get_user_locale(callback_query.from_user)
#     ).process_selection(callback_query, callback_data)
#     if selected:
#         await callback_query.message.answer(
#             f'You selected {date.strftime("%d/%m/%Y")}', reply_markup=start_kb
#         )


@router.message(F.text == "Забронировать столик")
async def form(message: Message, state: FSMContext):
    user_info = db.get_user_tg_id(message.from_user.id)
    if user_info is not None:
        await state.update_data(user_info=user_info)
        await message.answer("Введите кол-во человек:")
        await state.set_state(reserve_form.amount)
    else:
        await message.answer("Введите имя:")
        await state.set_state(reserve_form.name)


@router.message(reserve_form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отправтьте номер телефона ⬇️", reply_markup=get_phone_kb)
    await state.set_state(reserve_form.phone)


@router.message(F.contact, reserve_form.phone)
async def phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer("Введите кол-во человек:")
    await state.set_state(reserve_form.amount)


@router.message(reserve_form.amount)
async def amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await state.set_state(reserve_form.date)
    await message.answer(
        "Введите дату брони (не более недели вперед) в формате дд.мм.гггг:",
        reply_markup=get_date_kb(),
    )


@router.callback_query(DateCallback.filter(), reserve_form.date)
async def date(
    query: CallbackQuery, state: FSMContext, callback_data: DateCallback
):
    await state.update_data(date=callback_data.date)
    await message.answer("Введите время брони:")
    await state.set_state(reserve_form.time)


@router.message(reserve_form.time)
async def time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer("Оставтье комменатарий (либо -):")
    await state.set_state(reserve_form.comment)


@router.message(reserve_form.comment)
async def ps(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await confirm_message(message, state)
    await state.set_state(reserve_form.confirm)


async def confirm_message(message: Message, state: FSMContext):
    data = await state.get_data()
    if len(data) == 6:
        await message.answer(
            (
                f"Данные по бронированию:\n"
                f"<b>Имя</b>: {data['name']}\n"
                f"<b>Телефон для связи</b>: {data['phone']}\n"
                f"<b>кол-во человек</b>: {data['amount']}\n"
                f"<b>Дата брони</b>: {data['date']}\n"
                f"<b>Время брони</b>: {data['time']}\n"
                f"<b>Комментарий</b>: {data['comment']}\n"
            ),
            parse_mode="HTML",
            reply_markup=confirm_kb,
        )
    else:
        await message.answer(
            (
                f"Данные по бронированию:\n"
                f"<b>Имя</b>: {data['user_info'][0]}\n"
                f"<b>Телефон для связи</b>: {data['user_info'][1]}\n"
                f"<b>кол-во человек</b>: {data['amount']}\n"
                f"<b>Дата брони</b>: {data['date']}\n"
                f"<b>Время брони</b>: {data['time']}\n"
                f"<b>Комментарий</b>: {data['comment']}\n"
            ),
            parse_mode="HTML",
            reply_markup=confirm_kb,
        )

@router.message(F.text == "начать сначала", reserve_form.confirm)
async def start_over_handler(message: Message, state: FSMContext):
    await state.clear()
    user_info = db.get_user_tg_id(message.from_user.id)
    if user_info is not None:
        await state.update_data(user_info=user_info)
        await message.answer("Введите кол-во человек:")
        await state.set_state(reserve_form.amount)
    else:
        await message.answer("Введите имя:")
        await state.set_state(reserve_form.name)
    await state.set_state(reserve_form.name)


@router.message(F.text == "начать сначала", reserve_form.confirm)
async def start_over_handler(message: Message, state: FSMContext):
    await state.clear()
    user_info = db.get_user_tg_id(message.from_user.id)
    if user_info is not None:
        await state.update_data(user_info=user_info)
        await message.answer("Введите кол-во человек:")
        await state.set_state(reserve_form.amount)
    else:
        await message.answer("Введите имя:")
        await state.set_state(reserve_form.name)
    await state.set_state(reserve_form.name)


@router.message(F.text == "Подтвердить", reserve_form.confirm)
async def confirm_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer("Спасибо за вашу форму!")
    if len(data) == 6:
        db.insert_user(message.from_user.id, data["name"], data["phone"])
        db.insert_reserve(
            message.from_user.id,
            data["amount"],
            date_to_type(data['date'], data['time']),
            data["comment"],
        )
        await state.clear()
    else:
        db.insert_reserve(
            message.from_user.id,
            data["amount"],
            date_to_type(data['date'], data['time']),
            data["comment"],
        )


@router.message(F.text == "Написать кальянному мастеру")
async def send_phone(message: types.Message, state: FSMContext):
    await message.answer(
        """Напиши нам в [Telegram](https://t.me/Cs_Hookah)\nИли в [WhatsApp](https://wa.me/qr/SOVELK6ZAWY3D1)""",
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )
