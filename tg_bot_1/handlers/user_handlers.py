from copy import deepcopy
import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup


from tg_bot_1.lexicon.lexicon import LEXICON_RU, KEYBOARD_PRAMETERS, KEYBOARD_DOG_CAT
from tg_bot_1.database.database import user_dict_template, users_db
from tg_bot_1.keyboards.keyboard import create_keyboard

router = Router()

logger = logging.getLogger(__name__)

class FSMFillForm(StatesGroup):
    fill_dog = State()
    fill_LA = State()
    fill_Ao = State()


@router.message(CommandStart())
async def process_start_command(message, state):
    users_db[message.from_user.id] = deepcopy(user_dict_template)

    data = await state.get_data()
    attempt = data.get('num_attempt', 0)
    if attempt == 0:
        text = 'Your first attempt'
    else:
        text = f'Your {attempt} attempt'


    #LEXICON_RU['/start']

    await message.answer(
        text=text,
        reply_markup=create_keyboard(KEYBOARD_DOG_CAT,
                                            LEXICON_RU['width']))

    await state.update_data(attempt = attempt + 1)

    #await state.clear()
    val = await state.get_state()
    logger.info('%s', val)

    




@router.message(Command(commands=['help']))
async def process_help_command(message, state):
    await message.answer(LEXICON_RU['/help'])
    val = await state.get_state()
    logger.info('%s', val)


@router.callback_query(F.data == 'dog')
async def press_params(callback, state):
    await state.set_state(FSMFillForm.fill_dog)
    await callback.message.edit_text(
        text=LEXICON_RU['indicators'],
        reply_markup=create_keyboard(KEYBOARD_PRAMETERS,
                                            LEXICON_RU['width']))
    val = await state.get_state()
    logger.info('%s', val)


@router.callback_query(F.data == 'LA_button_pressed',
                       StateFilter(FSMFillForm.fill_dog))
async def press_la(callback, state):
    await state.set_state(FSMFillForm.fill_LA)
    await callback.message.edit_text(
        text='Введите значение ЛП'
    )
    val = await state.get_state()
    logger.info('%s', val)


@router.message(StateFilter(FSMFillForm.fill_LA))
async def press_la_val(message, state):
    users_db[message.from_user.id]['LA'] = int(message.text)
    await state.set_state(FSMFillForm.fill_dog)
    await message.answer(
        text=LEXICON_RU['indicators'],
        reply_markup=create_keyboard(KEYBOARD_PRAMETERS,
                                            LEXICON_RU['width']))
    val = await state.get_state()
    logger.info('%s', val)


@router.callback_query(F.data == 'Ao_button_pressed',
                       StateFilter(FSMFillForm.fill_dog))
async def press_ao(callback, state):
    await state.set_state(FSMFillForm.fill_Ao)
    await callback.message.edit_text(
        text='Введите значение Ао'
    )
    val = await state.get_state()
    logger.info('%s', val)


@router.message(StateFilter(FSMFillForm.fill_Ao))
async def press_ao_val(message, state):
    users_db[message.from_user.id]['Ao'] = int(message.text)
    await state.set_state(FSMFillForm.fill_dog)
    await message.answer(
        text=LEXICON_RU['indicators'],
        reply_markup=create_keyboard(KEYBOARD_PRAMETERS,
                                            LEXICON_RU['width']))
    val = await state.get_state()
    logger.info('%s', val)


@router.callback_query(F.data == 'count_up')
async def press_count(callback, state):
    Ao = users_db[callback.from_user.id]['Ao']
    LA = users_db[callback.from_user.id]['LA']
    await callback.message.edit_text(
        text=f'LA/Ao = {LA/Ao}'
    )
    val = await state.get_state()
    logger.info('%s', val)