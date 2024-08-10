from aiogram import Router

from tg_bot_1.lexicon.lexicon import LEXICON_RU


router = Router()

@router.message()
async def send_answer(message):
    await message.answer(LEXICON_RU['not_correct'])