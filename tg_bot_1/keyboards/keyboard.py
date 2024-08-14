from aiogram.types import InlineKeyboardButton # InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_keyboard(dict_params, width):
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    for text, button in dict_params.items():
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=button
        ))
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()