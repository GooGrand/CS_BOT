from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from state_list import item
from db import DataBase
from all_kb import (
    D,
    BACK,
    create_markup,
    discount_buttons,
    ItemCallback,
    PaymentCallback,
    master_kb,
    payment_kb,
)

router = Router()

db = DataBase()


@router.message(F.text == DISCOUNTERS)
async def select_item(message: Message, state: FSMContext):
    duty = db.get_active_duty()
    await state.update_data(duty_id=duty[2])
    if duty[2] == message.from_user.id:
        buttons = discount_buttons()
        markup = create_markup(buttons)
        await message.answer("Обоснуй че продал", reply_markup=markup)
    else:
        await message.answer("Не твоя смена")


@router.callback_query(DiscountCallback.filter())
async def apply_expense(
    query: CallbackQuery, state: FSMContext, callback_data: ExpensesCallback
):
    data = await state.get_data()
    db.insert_buy(callback_data["item_id"], data["master_id"], 'transfer', '')
    await message.answer("Имей сто рублей")