from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from state_list import item, expenses
from db import DataBase
from all_kb import (
    EXPENSES,
    create_markup,
    select_item_buttons,
    ItemCallback,
    PaymentCallback,
    ExpensesCallback,
    master_kb,
    payment_kb,
    expense_kb,
    stats_kb,
)
from aiogram.filters import Command

router = Router()

db = DataBase()



@router.message(F.text == EXPENSES)
async def select_expense(message: Message, state: FSMContext):
    # duty = db.get_active_duty()
    # if duty[2] == message.from_user.id:
    #     buttons = select_item_buttons()
    #     markup = select_item_markup(buttons)
    #     await state.set_state(item.apply)
    #     await message.answer("Обоснуй че продал", reply_markup=markup)
    # else:
    #     await message.answer("Не твоя смена")
    await message.answer("на что потратили", reply_markup=expense_kb)
    await state.set_state(expenses.apply)


@router.callback_query(ExpensesCallback.filter(), expenses.apply)
async def apply_expense(
    query: CallbackQuery, state: FSMContext, callback_data: ExpensesCallback
):
    await state.update_data(expense=callback_data.expense_type)
    await state.set_state(expenses.amount)
    await query.message.answer("Сколько?")


@router.message(expenses.amount)
async def amount_expense(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await state.set_state(expenses.comment)
    await message.answer("Добавишь коммент?")


@router.message(expenses.comment)
async def confirm_expense(message: Message, state: FSMContext):
    data = await state.get_data()
    db.insert_expense(data["expense"], int(data["amount"]), message.text)
    await state.set_state(None)
    await message.answer("хрш хрш браза")