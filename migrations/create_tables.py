# Для запуска миграций из контейнера, когда в постгрес и редис хосты указаны по названию:
# docker-compose exec bot python -m migrations.create_tables
# Добавил в докерфайл строку для запуска сначала миграций, автоматически. Сейчас не нужно отдельно
# docker compose build bot
# docker compose up -d bot
import asyncio
import logging
import os
import sys

from app.infrastructure.database.connection import get_pg_connection
from config.config import Config, load_config
from psycopg import AsyncConnection, Error

config: Config = load_config()

logging.basicConfig(
    level=logging.getLevelName(level=config.log.level),
    format=config.log.format,
)

logger = logging.getLogger(__name__)

# Настройка цикла событий для Windows
if sys.platform.startswith("win") or os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    connection: AsyncConnection | None = None

    try:
        connection = await get_pg_connection(
            db_name=config.db.name,
            host=config.db.host,
            port=config.db.port,
            user=config.db.user,
            password=config.db.password,
        )
        async with connection:
            async with connection.transaction():
                async with connection.cursor() as cursor:
                    # Таблица пользователей
                    await cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS users(
                            id SERIAL PRIMARY KEY,
                            user_id BIGINT NOT NULL UNIQUE,
                            username VARCHAR(50),
                            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                            role VARCHAR(30) NOT NULL,
                            is_alive BOOLEAN NOT NULL,
                            banned BOOLEAN NOT NULL
                        );
                        """
                    )
                    # Таблица профилей пользователей
                    await cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS users_profiles(
                            user_id BIGINT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
                            gender VARCHAR(20) NOT NULL,
                            age SMALLINT,
                            height SMALLINT,
                            weight SMALLINT,
                            goal VARCHAR(50) NOT NULL,
                            activity VARCHAR(50) NOT NULL,
                            diet TEXT NOT NULL,
                            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                        );
                        """
                    )
                    # Таблица для хранения суточных норм пользователей после подсчета от ии
                    await cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS users_nutrition_limits (
                            user_id BIGINT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
                            calories INT NOT NULL,
                            protein_grams INT  NOT NULL,
                            fat_grams INT  NOT NULL,
                            carbs_grams INT  NOT NULL,
                            fiber_grams INT NOT NULL,
                            omega3_mg INT,
                            potassium_mg INT,
                            magnesium_mg INT,
                            sodium_mg INT,
                            calculated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                        );
                        """
                    )
                logger.info("Tables 'users', 'users_profiles' were successfully created")
    except Error as db_error:
        logger.exception("Database-specific error: %s", db_error)
    except Exception as e:
        logger.exception("Unhandled error: %s", e)
    finally:
        if connection:
            await connection.close()
            logger.info("Connection to Postgres closed")

asyncio.run(main())
