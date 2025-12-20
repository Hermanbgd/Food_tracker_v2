import asyncio
import logging

from aiogram.types import Message

logger = logging.getLogger(__name__)

# Вспомогательная функция для удаления сообщения через delay секунд
async def delete_after(msg: Message, delay: int = 5):
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except Exception as e:
        logger.warning(f"Не удалось удалить сообщение: {e}")