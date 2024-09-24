from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_objects, get_item_by_object

main = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Объекты')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню'
)


def main_button():
    return InlineKeyboardButton(text='На главную',
                                callback_data='go_main')


def edit_button(item_id):
    return InlineKeyboardButton(text='Редактировать',
                                callback_data=f'edit_item_{item_id}')


async def objects():
    all_objects = await get_objects()
    keyboard = InlineKeyboardBuilder()
    for obj in all_objects:
        keyboard.add(InlineKeyboardButton(text=obj.name,
                                          callback_data=f'object_{obj.id}'))
    return keyboard.adjust(2).as_markup()


async def items(object_id):
    all_items = await get_item_by_object(object_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.number,
                                          callback_data=f'item_{item.id}'))
    keyboard.add(main_button())
    return keyboard.adjust(2).as_markup()


def edit_item_keyboard(item_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text='Категория',
                             callback_data=f'edit_field_category_{item_id}'),
        InlineKeyboardButton(text='Документация',
                             callback_data=f'edit_field_documentation_{item_id}')
    )
    keyboard.row(
        InlineKeyboardButton(text='Описание',
                             callback_data=f'edit_field_description_{item_id}'),
        InlineKeyboardButton(text='Номинальный Ампераж',
                             callback_data=f'edit_field_amperage_{item_id}')
    )
    keyboard.row(
        InlineKeyboardButton(text='Статус',
                             callback_data=f'edit_field_status_{item_id}'),
        InlineKeyboardButton(text='Текущий Ампераж',
                             callback_data=f'edit_field_current_amperage_{item_id}')
    )
    keyboard.row(
        InlineKeyboardButton(text='Отмена',
                             callback_data=f'cancel_{item_id}')
    )
    return keyboard.as_markup()
