from aiogram import Router
from aiogram.filters import Command

from tg_bot_1.lexicon.lexicon import LEXICON_RU

router = Router()

@router.message(Command(commands=['start', 'help']))
async def process_start_command(message):
    await message.answer(LEXICON_RU['/start'])