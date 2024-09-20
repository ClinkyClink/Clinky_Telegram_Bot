import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from app.keyboards import main, items, objects, edit_item_keyboard, main_button, edit_button
from app.database import requests as rq
from app.utils import get_object_name

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()


class EditItem(StatesGroup):
    waiting_for_field = State()
    waiting_for_new_value = State()

fields = {
    'category': 'Категория',
    'documentation': 'Документация',
    'description': 'Описание',
    'amperage': 'Ампераж',
    'status': 'Статус',
    'current_amperage': 'Текущий ампераж',
}

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(f'Привет {message.from_user.first_name}',
                         reply_markup=main)

@router.message(F.text == 'Объекты')
async def list_object(message: Message):
    await message.answer('Выберите объект', reply_markup=await objects())

@router.callback_query(F.data.startswith('object_'))
async def object_list(callback: CallbackQuery):
    object_id = callback.data.split('_')[1]
    object_name = await get_object_name(object_id)
    await callback.answer('Вы выбрали объект')
    await callback.message.answer(f'Выберите скважину на объекте {object_name}',
                                  reply_markup=await items(object_id))

@router.callback_query(F.data.startswith('item_'))
async def show_item(callback: CallbackQuery):
    item_id = callback.data.split('_')[1]
    item_data = await rq.get_item(item_id)
    await callback.answer('Вы выбрали скважину')
    buttons_list = [[main_button()], [edit_button(item_data.id)]]
    main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons_list)
    await callback.message.answer(
        f'{item_data.number}\n'
        f'Станция: {item_data.category.name}\n'
        f'Руководство: {item_data.category.documentation}\n'
        f'Описание: {item_data.description}\n'
        f'Номинальный ампераж: {str(item_data.amperage) + "A" if item_data.amperage != "-" else "Нет данных"}\n'
        f'Статус: {item_data.status}\n'
        f'Текущий ампераж: {item_data.current_amperage}\n',
        reply_markup=main_menu_keyboard
    )

@router.callback_query(F.data.startswith('edit_item_'))
async def on_edit_button(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    item_id = int(callback_query.data.split('_')[2])
    await state.update_data(item_id=item_id)
    await callback_query.bot.send_message(
        chat_id=callback_query.message.chat.id,
        text='Выберите поле для изменения:', 
        reply_markup=edit_item_keyboard(item_id)
    )
    await state.set_state(EditItem.waiting_for_field)

@router.callback_query(F.data.startswith('edit_field_'))
async def edit_field(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    field_name = data[2]
    if data[3].isdigit():
        item_id = int(data[3])
    elif data[4].isdigit():
        item_id = int(data[4])
        if field_name == 'current':
            field_name = 'current_amperage'
    else:
        print(f'Ошибка: {data[3]} не является числом')
    item_data = await rq.get_item(item_id)
    current_value = getattr(item_data, field_name, 'Нет данных')
    await state.update_data(field_name=field_name, item_id=item_id)
    await callback.message.edit_text(
        f'Введите новое значение для {fields[field_name]}\n'
        f'Текущее значение: {current_value}',
        reply_markup=None
    )
    await callback.answer()
    await state.set_state(EditItem.waiting_for_new_value)

@router.message(EditItem.waiting_for_new_value)
async def handle_new_value(message: Message, state: FSMContext):
    data = await state.get_data()
    item_id = data.get('item_id')
    field_name = data.get('field_name')
    new_value = message.text.strip()
    logging.info(f'Пользователь {message.from_user.id} изменяет поле {field_name} для item_id {item_id} на "{new_value}"')
    await rq.update_field(item_id, field_name, new_value)
    await message.answer(f'{fields[field_name]} изменена на "{new_value}".')
    await state.clear()
    item_data = await rq.get_item(item_id)
    buttons_list = [[main_button()], [edit_button(item_data.id)]]
    main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons_list)
    await message.answer(
        f'{item_data.number}\n'
        f'Станция: {item_data.category.name}\n'
        f'Руководство: {item_data.category.documentation}\n'
        f'Описание: {item_data.description}\n'
        f'Номинальный ампераж: {str(item_data.amperage) + "A" if isinstance(item_data.amperage, (int, float)) else "Нет данных"}\n'
        f'Статус: {item_data.status}\n'
        f'Текущий ампераж: {item_data.current_amperage}\n',
        reply_markup=main_menu_keyboard
    )

@router.callback_query(F.data.startswith('cancel_'))
async def cancel_edit(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.clear()
    await callback_query.message.edit_text(
        'Редактирование отменено.',
        reply_markup=await objects()
    )

@router.callback_query(F.data == 'go_main')
async def on_main_button(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.bot.send_message(text='Вы вернулись на главную',
                                          chat_id=callback_query.from_user.id,
                                          reply_markup=await objects())
