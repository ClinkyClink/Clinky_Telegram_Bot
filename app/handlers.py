from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb
import app.database.requests as rq


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(f'Привет {message.from_user.first_name}',
                         reply_markup=kb.main)


@router.message(F.text == 'Объекты')
async def list_object(message: Message):
    await message.answer('Выберите объект', reply_markup=await kb.objects())


@router.callback_query(F.data.startswith('object_'))
async def object_list(callback: CallbackQuery):
    await callback.answer('Вы выбрали объект')
    await callback.message.answer('Выберите скважину на объекте',
                                  reply_markup=await kb.items(
                                      callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def object(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('Вы выбрали скважину')
    await callback.message.answer(
        f'{item_data.number}\n'
        f'Станция: {item_data.category.name}\n'
        f'Описание: {item_data.description}\n'
        f'Ампераж: {item_data.amperage}A',
        reply_markup=await kb.items(callback.data.split('_')[1])
    )


@router.callback_query(F.data == 'go_main')
async def on_main_button(callback_query: CallbackQuery):
    await callback_query.message.edit_text('Вы вернулись на главную',
                                           reply_markup=await kb.objects())
