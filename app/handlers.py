from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет {message.from_user.first_name}')


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Это команда /help')