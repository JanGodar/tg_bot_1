from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup


from tg_bot_1.lexicon.lexicon import LEXICON_RU, KEYBOARD_PRAMETERS, KEYBOARD_DOG_CAT
from tg_bot_1.database.database import user_dict_template, users_db
from tg_bot_1.keyboards.keyboard import create_keyboard

router = Router()

class FSMFillForm(StatesGroup):
    fill_Ao = State()
    fill_LA = State()


@router.message(CommandStart())
async def process_start_command(message):
    users_db[message.from_user.id] = deepcopy(user_dict_template)
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=create_keyboard(KEYBOARD_DOG_CAT,
                                            LEXICON_RU['width']))


@router.message(Command(commands=['help']))
async def process_help_command(message):
    await message.answer(LEXICON_RU['/help'])


# @router.callback_query(F.data == 'Ao_button_pressed')
# async def press_ao(message, state):
#     await message.answer('Введите значение')
#     await state.set_state(FSMFillForm.fill_Ao)


# @router.callback_query(StateFilter(FSMFillForm.fill_Ao))
# async def Ao(message, state):
#     users_db[message.from_user.id]['Ao'] = message.text
#     await state.clear()