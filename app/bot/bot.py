import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window, StartMode, setup_dialogs
from aiogram_dialog.api.entities import ShowMode  # Для DELETE_AND_SEND (опционально)
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Column, Row, Button, Back, Cancel, Multiselect
from aiogram_dialog.widgets.text import Format, Const

import psycopg_pool
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder

from app.bot.dialogs.dialog_menu import main_menu
from app.bot.dialogs.dialog_profile import create_profile
from app.bot.handlers.users import user_router
from app.bot.middlewares.database import DataBaseMiddleware
# from app.bot.handlers.admin import admin_router
# from app.bot.handlers.others import others_router
# from app.bot.handlers.user import user_router
# from app.bot.middlewares.database import DataBaseMiddleware
# from app.bot.middlewares.shadow_ban import ShadowBanMiddleware
# from app.bot.middlewares.throttle import ThrottleMiddleware
from app.infrastructure.database.connection import get_pg_pool
from config.config import Config
from redis.asyncio import Redis


logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main(config: Config) -> None:
    logger.info("Starting bot...")
    # Инициализируем хранилище
    storage = RedisStorage(
        redis=Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            password=config.redis.password,
            username=config.redis.username,
        ),
        key_builder = DefaultKeyBuilder(with_destiny=True),
    )

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    # Создаём пул соединений с Postgres
    db_pool: psycopg_pool.AsyncConnectionPool = await get_pg_pool(
        db_name=config.db.name,
        host=config.db.host,
        port=config.db.port,
        user=config.db.user,
        password=config.db.password,
    )


    # Подключаем роутеры в нужном порядке
    logger.info("Including routers...")
    # dp.include_routers(admin_router, user_router, others_router)
    dp.include_routers(user_router, main_menu, create_profile)
    setup_dialogs(dp)

    # Подключаем миддлвари в нужном порядке
    logger.info("Including middlewares...")
    dp.update.outer_middleware(DataBaseMiddleware(pool=db_pool))
    dp.callback_query.outer_middleware(DataBaseMiddleware(pool=db_pool))
    # dp.update.middleware(ShadowBanMiddleware())
    # dp.update.middleware(ThrottleMiddleware(max_messages=5, window_seconds=10))


    # Запускаем поллинг
    try:
        await dp.start_polling(
            bot, db_pool=db_pool,
            admin_ids=config.bot.admin_ids
        )
    except Exception as e:
        logger.exception(e)
    finally:
        # Закрываем пул соединений
        await db_pool.close()
        logger.info("Connection to Postgres closed")