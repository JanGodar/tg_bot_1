from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup


from tg_bot_1.lexicon.lexicon import LEXICON_RU, KEYBOARD_PRAMETERS, KEYBOARD_DOG_CAT
from tg_bot_1.database.database import user_dict_template, users_db
from tg_bot_1.keyboards.keyboard import create_keyboard

router = Router()

class FSMFillForm(StatesGroup):
    fill_dog = State()
    fill_LA = State()
    fill_Ao = State()


@router.message(CommandStart())
async def process_start_command(message):
    users_db[message.from_user.id] = deepcopy(user_dict_template)
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=create_keyboard(KEYBOARD_DOG_CAT,
                                            LEXICON_RU['width']))
        #?  await state.clear()


@router.message(Command(commands=['help']))
async def process_help_command(message):
    await message.answer(LEXICON_RU['/help'])


@router.callback_query(F.data == 'dog')
async def press_params(callback, state):
    await state.set_state(FSMFillForm.fill_dog)
    await callback.message.edit_text(
        text=LEXICON_RU['indicators'],
        reply_markup=create_keyboard(KEYBOARD_PRAMETERS,
                                            LEXICON_RU['width']))


@router.callback_query(F.data == 'LA_button_pressed',
                       StateFilter(FSMFillForm.fill_dog))
async def press_la(callback, state):
    await state.set_state(FSMFillForm.fill_LA)
    await callback.message.edit_text(
        text='Введите значение ЛП'
    )


@router.message(StateFilter(FSMFillForm.fill_LA))
async def press_la_val(message, state):
    users_db[message.from_user.id]['LA'] = int(message.text)
    await state.set_state(FSMFillForm.fill_dog)
    await message.answer(
        text=LEXICON_RU['indicators'],
        reply_markup=create_keyboard(KEYBOARD_PRAMETERS,
                                            LEXICON_RU['width']))


@router.callback_query(F.data == 'Ao_button_pressed',
                       StateFilter(FSMFillForm.fill_dog))
async def press_ao(callback, state):
    await state.set_state(FSMFillForm.fill_Ao)
    await callback.message.edit_text(
        text='Введите значение Ао'
    )


@router.message(StateFilter(FSMFillForm.fill_Ao))
async def press_ao_val(message, state):
    users_db[message.from_user.id]['Ao'] = int(message.text)
    await state.set_state(FSMFillForm.fill_dog)
    await message.answer(
        text=LEXICON_RU['indicators'],
        reply_markup=create_keyboard(KEYBOARD_PRAMETERS,
                                            LEXICON_RU['width']))


@router.callback_query(F.data == 'count_up')
async def press_count(callback, state):
    Ao = users_db[callback.from_user.id]['Ao']
    LA = users_db[callback.from_user.id]['LA']
    await callback.message.edit_text(
        text=f'LA/Ao = {LA/Ao}'
    )

# @router.message(StateFilter(FSMFillForm.fill_count))
# async def press_ao(message, state):
#     users_db[message.from_user.id]['LA'] = int(message.text)
#     await message.answer('Введите значение Ао')


# @router.message(StateFilter(FSMFillForm.fill_count))
# async def return_to_press(message, state):
#     users_db[message.from_user.id]['Ao'] = int(message.text)
#     await state.set_state(FSMFillForm.fill_count)
#     await message.answer(
#         text='Продолжайте заполнение значений, либо жмите посчитать',
#         reply_markup=create_keyboard(KEYBOARD_DOG_CAT,
#                                             LEXICON_RU['width']))

#     users_db[message.from_user.id]['LA'] = int(message.text)
#     print(users_db[message.from_user.id]['LA'])

# await message.answer(text='Введите значение ЛП')
    


# @router.callback_query(StateFilter(FSMFillForm.fill_Ao))
# async def Ao(message, state):
#     users_db[message.from_user.id]['Ao'] = message.text
#     await state.clear()