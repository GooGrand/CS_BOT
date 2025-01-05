from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from state_list import item
from db import DataBase
from all_kb import (
    SELL,
    BACK,
    create_markup,
    select_item_buttons,
    ItemCallback,
    PaymentCallback,
    master_kb,
    payment_kb,
)

router = Router()

db = DataBase()

@router.message(F.text == SELL)
async def select_item(message: Message, state: FSMContext):
    duty = db.get_active_duty()
    await state.update_data(duty_id=duty[2])
    if duty[2] == message.from_user.id:
        buttons = select_item_buttons()
        markup = create_markup(buttons)
        await state.set_state(item.apply)
        await message.answer("Обоснуй че продал", reply_markup=markup)
    else:
        await message.answer("Не твоя смена")

@router.callback_query(ItemCallback.filter(), item.apply)
async def apply_item(
    query: CallbackQuery, state: FSMContext, callback_data: ItemCallback
):
    await state.update_data(item_id=callback_data.item_id)
    await state.set_state(item.payment)
    await query.message.answer("Какая оплата", reply_markup=payment_kb)


@router.callback_query(PaymentCallback.filter(), item.payment)
async def comment_item(
    query: CallbackQuery, state: FSMContext, callback_data: PaymentCallback
):
    await state.update_data(payment=callback_data.payment_type)
    await state.set_state(item.comment)
    await query.message.answer("Добавишь коммент?")


@router.message(item.comment)
async def confirm_item(message: Message, state: FSMContext):
    data = await state.get_data()
    db.insert_buy(data["item_id"], data["master_id"], data["payment"], message.text)
    await state.set_state(None)
    await state.update_data(item_id=None)
    await state.update_data(payment=None)
    await message.answer("Имей сто рублей")