from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from db import DataBase
from state_list import contact
from all_kb import (
    SELL,
    SEE_SALARY,
    SEE_INCOME,
    OPEN,
    GET_MONTH_SALARY,
    create_markup,
    select_item_buttons,
    ItemCallback,
    PaymentCallback,
    master_kb,
    payment_kb,
)
from aiogram.filters import Command

router = Router()

db = DataBase()


@router.message_handler(F.text == "отправить контакт")
async def get_age(message: types.Message, state: FSMContext):
    await state.set_state(contact.send)


@router.message_handler(contact.send, content_types=types.ContentType.CONTACT)
async def contacts(message: types.Message, state: FSMContext):
    await message.answer(
        f"Твой номер успешно получен: {message.contact.phone_number}",
    )
    await state.finish()
