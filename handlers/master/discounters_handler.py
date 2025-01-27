from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from state_list import item
from db import DataBase
from all_kb import (
    DISCOUNTERS,
    DiscountCallback,
    ExpensesCallback,
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
    if duty is None:
        await message.answer("Смену открой придурок")
    await state.update_data(duty_id=duty[0])
    if duty[1] == message.from_user.id:
        buttons = discount_buttons()
        markup = create_markup(buttons)
        await state.set_state(item.discounters)
        await message.answer("Выборы выборы...", reply_markup=markup)
    else:
        await message.answer("Не твоя смена")


@router.callback_query(DiscountCallback.filter())
async def apply_expense(
    query: CallbackQuery, state: FSMContext, callback_data: DiscountCallback
):
    data = await state.get_data()
    db.insert_buy(callback_data.item_id, query.from_user.id, 'transfer', '', callback_data.name)
    await state.set_state(None)
    await query.message.answer("Имей сто рублей")