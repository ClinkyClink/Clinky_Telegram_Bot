from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_objects, get_item_by_object

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Объекты')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню')


async def objects():
    all_objects = await get_objects()
    keyboard = InlineKeyboardBuilder()
    for object in all_objects:
        keyboard.add(InlineKeyboardButton(text=object.name,
                                          callback_data=f'object_{object.id}'))
    return keyboard.adjust(2).as_markup()


async def items(object_id):
    all_items = await get_item_by_object(object_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.number,
                                          callback_data=f'item_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='go_main'))
    return keyboard.adjust(2).as_markup()
