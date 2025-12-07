from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from psycopg import AsyncConnection

from app.bot.enums.roles import UserRole
from app.bot.states_dialogs.states_menu import MainMenu
from app.infrastructure.database.db import get_user, add_user, change_user_alive_status

# Инициализируем роутер уровня модуля
user_router = Router()

# Этот хэндлер срабатывает на команду /start
@user_router.message(CommandStart())
async def command_start_process(
    message: Message,
    dialog_manager: DialogManager,
    bot: Bot,
    conn: AsyncConnection,
    state: FSMContext,
    admin_ids: list[int]
):
    user_row = await get_user(conn, user_id=message.from_user.id)
    if user_row is None:
        user_role = UserRole.ADMIN if message.from_user.id in admin_ids else UserRole.USER
        await add_user(conn, user_id=message.from_user.id, username=message.from_user.username, role=user_role)
    else:
        user_role = UserRole(user_row[3])
        await change_user_alive_status(conn, is_alive=True, user_id=message.from_user.id)

    await dialog_manager.start(state=MainMenu.menu, mode=StartMode.RESET_STACK)

