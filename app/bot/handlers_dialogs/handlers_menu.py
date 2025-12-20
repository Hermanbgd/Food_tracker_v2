import asyncio
import logging

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from app.bot.services.ai_service import get_food_description
from app.bot.services.other_functions import delete_after
from app.bot.services.v_t_t_service import transcribe_voice_message
from app.bot.states_dialogs.states_menu import MainMenu
from app.bot.states_dialogs.states_profile import ProfileSetSG
from app.infrastructure.database.db import add_food_db, add_food_analysis

logger = logging.getLogger(__name__)


async def add_food(callback:CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=MainMenu.food_add)

async def view_food(callback: CallbackQuery, button:Button, dialog_manager: DialogManager):
    await callback.answer()


async def go_profile(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=MainMenu.profile)

async def set_profile(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=ProfileSetSG.gender, mode=StartMode.RESET_STACK)

# async def go_main_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
#     await dialog_manager.start(state=MainMenu.menu, mode=StartMode.RESET_STACK)

async def go_main_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=MainMenu.menu)

async def handle_food_input(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
):
    conn = dialog_manager.middleware_data["conn"]
    user_id = dialog_manager.event.from_user.id
    if message.text:
        logger.info(f"Получено текстовое сообщение от пользователя {message.from_user.id}")
        user_mes = message.text
    elif message.voice:
        # отправляем временное сообщение
        sent_trans = await message.answer("Распознаю голосовое сообщение...")

        # Преобразование голосового сообщения в текст
        logger.info(f"Получено голосовое сообщение от пользователя {message.from_user.id}")
        user_mes = await transcribe_voice_message(message.bot, message.voice.file_id)
        logger.info(f"Преобразованное текстовое сообщение: {user_mes}")

        await message.bot.delete_message(chat_id=message.chat.id, message_id=sent_trans.message_id)
    else:
        # Временное предупреждение, которое исчезнет через 5 секунд
        temp_msg = await message.answer(
            "Пожалуйста, отправь текст или голосовое сообщение о приёме пищи."
        )
        # Запланируем удаление через 5 секунд
        asyncio.create_task(delete_after(temp_msg, delay=5))
        return

    await add_food_db(conn, user_id=user_id, food=user_mes)

    food_description_llm = await get_food_description(user_mes)

    await add_food_analysis(conn,
                            user_id=user_id,
                            calories=food_description_llm["calories"],
                            protein_grams=food_description_llm["protein_grams"],
                            fat_grams=food_description_llm["fat_grams"],
                            carbs_grams=food_description_llm["carbs_grams"],
                            fiber_grams=food_description_llm["fiber_grams"],
                            omega3_mg=food_description_llm["omega3_mg"],
                            potassium_mg=food_description_llm["potassium_mg"],
                            magnesium_mg=food_description_llm["magnesium_mg"],
                            sodium_mg=food_description_llm["sodium_mg"])


    # Подтверждение, которое тоже исчезнет через 7 секунд
    success_msg = await message.answer(f"Приём пищи зафиксирован: {user_mes}")

    # Удаляем подтверждение через 7 секунд
    asyncio.create_task(delete_after(success_msg, delay=6))

    # Вернись в главное меню или другое состояние
    # await manager.switch_to(MainMenu.menu)  # или manager.done() / manager.start(...)