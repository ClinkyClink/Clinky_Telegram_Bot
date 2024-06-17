from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import app.keyboards as kb
import app.database.requests as rq


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(f'Привет {message.from_user.first_name}')
