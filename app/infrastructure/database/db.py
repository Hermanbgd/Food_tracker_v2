import logging
from datetime import datetime, timezone
from typing import Any, Optional

from app.bot.enums.roles import UserRole
from psycopg import AsyncConnection

logger = logging.getLogger(__name__)

async def add_user(
    conn: AsyncConnection,
    *,
    user_id: int,
    username: str | None = None,
    role: UserRole = UserRole.USER,
    is_alive: bool = True,
    banned: bool = False,
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
                INSERT INTO users(user_id, username, role, is_alive, banned)
                VALUES(
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s
                ) ON CONFLICT (user_id) DO NOTHING;
            """,
            (
                user_id,
                username,
                role,
                is_alive,
                banned,
            ),
        )
    logger.info(
        "User added. Table=`%s`, user_id=%d, created_at='%s', "
        "role=%s, is_alive=%s, banned=%s",
        "users",
        user_id,
        datetime.now(timezone.utc),
        role,
        is_alive,
        banned,
    )

async def get_user(
    conn: AsyncConnection,
    *,
    user_id: int,
) -> tuple[Any, ...] | None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
                SELECT 
                    id,
                    user_id,
                    username,
                    role,
                    is_alive,
                    banned,
                    created_at
                    FROM users WHERE user_id = %s;
            """,
            (user_id,),
        )
        row = await cursor.fetchone()
    logger.info("Row is %s", row)
    return row if row else None


async def change_user_alive_status(
    conn: AsyncConnection,
    *,
    is_alive: bool,
    user_id: int,
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
                UPDATE users
                SET is_alive = %s
                WHERE user_id = %s;
            """,
            (is_alive, user_id)
        )
    logger.info("Updated `is_alive` status to `%s` for user %d", is_alive, user_id)


async def change_user_banned_status_by_id(
    conn: AsyncConnection,
    *,
    banned: bool,
    user_id: int,
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
                UPDATE users
                SET banned = %s
                WHERE user_id = %s
            """,
            (banned, user_id)
        )
    logger.info("Updated `banned` status to `%s` for user %d", banned, user_id)


async def change_user_banned_status_by_username(
    conn: AsyncConnection,
    *,
    banned: bool,
    username: str,
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
                UPDATE users
                SET banned = %s
                WHERE username = %s
            """,
            (banned, username)
        )
    logger.info("Updated `banned` status to `%s` for username %s", banned, username)


async def get_user_alive_status(
    conn: AsyncConnection,
    *,
    user_id: int,
) -> bool | None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
                SELECT is_alive FROM users WHERE user_id = %s;
            """,
            (user_id,),
        )
        row = await cursor.fetchone()
    if row:
        logger.info("The user with `user_id`=%s has the is_alive status is %s", user_id, row[0])
    else:
        logger.warning("No user with `user_id`=%s found in the database", user_id)
    return row[0] if row else None


async def get_user_banned_status_by_id(
    conn: AsyncConnection,
    *,
    user_id: int,
) -> bool | None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
                SELECT banned FROM users WHERE user_id = %s;
            """,
            (user_id,),
        )
        row = await cursor.fetchone()
    if row:
        logger.info("The user with `user_id`=%s has the banned status is %s", user_id, row[0])
    else:
        logger.warning("No user with `user_id`=%s found in the database", user_id)
    return row[0] if row else None


async def get_user_banned_status_by_username(
    conn: AsyncConnection,
    *,
    username: str,
) -> bool | None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
                SELECT banned FROM users WHERE username = %s;
            """,
            (username,),
        )
        row = await cursor.fetchone()
    if row:
        logger.info("The user with `username`=%s has the banned status is %s", username, row[0])
    else:
        logger.warning("No user with `username`=%s found in the database", username)
    return row[0] if row else None


async def get_user_role(
    conn: AsyncConnection,
    *,
    user_id: int,
) -> UserRole | None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
                SELECT role FROM users WHERE user_id = %s;
            """,
            (user_id,),
        )
        row = await cursor.fetchone()
    if row:
        logger.info("The user with `user_id`=%s has the role is %s", user_id, row[0])
        return UserRole(row[0])
    else:
        logger.warning("No user with `user_id`=%s found in the database", user_id)
    return None


async def add_user_profile(conn: AsyncConnection,
                           user_id: int,
                           gender: str,
                           age: str,
                           height: str,
                           weight: str,
                           goal: str,
                           activity: str,
                           diet: str) -> None:
    async with conn.transaction():
        async with conn.cursor() as cursor:
            # Добавляем данные профиля
            await cursor.execute(
                """
                INSERT INTO users_profiles (
                    user_id, gender, age, height, weight, goal, activity, diet, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW())
                ON CONFLICT (user_id) 
                DO UPDATE SET
                    gender = EXCLUDED.gender,
                    age = EXCLUDED.age,
                    height = EXCLUDED.height,
                    weight = EXCLUDED.weight,
                    goal = EXCLUDED.goal,
                    activity = EXCLUDED.activity,
                    diet = EXCLUDED.diet,
                    updated_at = NOW();
                """,
                (user_id, gender, age, height, weight, goal, activity, diet)
            )

async def get_user_profile(
    conn: AsyncConnection,
    *,
    user_id: int,
) -> tuple[Any, ...] | None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
                SELECT 
                    gender,
                    age,
                    height,
                    weight,
                    goal,
                    activity,
                    diet
                    FROM users_profiles WHERE user_id = %s;
            """,
            (user_id,),
        )
        row = await cursor.fetchone()
    logger.info("Row is %s", row)
    return row if row else None


