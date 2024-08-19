import logging
from aiogram import Router

from tg_bot_1.lexicon.lexicon import LEXICON_RU

logger = logging.getLogger(__name__)

router = Router()

@router.message()
async def send_answer(message, state):
    await message.answer(LEXICON_RU['not_correct'])
    val = await state.get_state()
    logger.info('%s', val)