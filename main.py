import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from tg_bot_1.config_data.config import BotSettings
from tg_bot_1.handlers import user_handlers, other_handlers
from tg_bot_1.keyboards.set_menu import set_main_menu


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='{filename}:{lineno} #{levelname:8} '
               '[{asctime}] - {name} - {message}',
        style='{'
    )

    logger.info('Starting bot')

    settings = BotSettings()

    bot = Bot(token=settings.bot_token.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = RedisStorage.from_url(str(settings.redis_dsn))
    dp = Dispatcher(storage=storage)

    logger.info('Add routers')
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())