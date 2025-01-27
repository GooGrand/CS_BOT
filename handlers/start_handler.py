from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from all_kb import start_kb, master_kb
from db import DataBase

db = DataBase()
router = Router()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    if db.get_hookah_master(message.from_user.id):
        # await state.update_data(master_id=master_id)
        # update duty if exists
        await message.answer("Здарова мистер кальянщик", reply_markup=master_kb)
    else:
        await message.answer("Брони, акции и всякое интересное", reply_markup=start_kb)


@router.message(Command("my_id"))
async def start(message: Message):
    await message.answer(f"Твой айди: {message.from_user.id}", reply_markup=start_kb)
