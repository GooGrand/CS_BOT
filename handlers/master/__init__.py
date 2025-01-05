from aiogram import F, Router

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from all_kb import (
    BACK,
    master_kb,
)

import handlers.master.sell_handler
import handlers.master.stats_handler
import handlers.master.discounters_handler

router = Router()


router.include_router(sell_handler.router)
router.include_router(stats_handler.router)
router.include_router(discounters_handler.router)

@router.message(F.text == BACK)
async def stats(message: Message, state: FSMContext):
    await message.answer("Ага", reply_markup=master_kb)