import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update
from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)


class DataBaseMiddleware(BaseMiddleware):
    def __init__(self, pool: AsyncConnectionPool):
        self.pool = pool  # ← сохранили пул

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        # ← БЕРЁМ ПУ ПУЛ ИЗ self.pool, а не из data["db_pool"]!!!
        async with self.pool.connection() as connection:
            async with connection.transaction():
                data["conn"] = connection                 # ← вот он, твой conn
                try:
                    result = await handler(event, data)
                    return result
                except Exception as e:
                    logger.exception("Transaction rolled back: %s", e)
                    raise