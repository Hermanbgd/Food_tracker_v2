from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from app.bot.states_dialogs.states_menu import MainMenu
from app.bot.states_dialogs.states_profile import ProfileSetSG


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
    manager: DialogManager,
):
    if message.text:
        description = message.text
    elif message.voice:
        # Здесь можешь скачать voice и транскрибировать (например, через Whisper или другой сервис)
        # Пример заглушки:
        description = "[Голосовое сообщение получено, транскрипция в разработке]"
        # await message.voice.download(...) для обработки файла
    else:
        await message.alert("Пожалуйста, отправь текст или голосовое сообщение о приёме пищи.")
        return

    # Здесь твоя логика обработки (добавление еды, AI-анализ и т.д.)
    # Например, сохрани в dialog_data:
    manager.dialog_data["food_description"] = description

    await message.alert(f"Приём пищи записан: {description}")

    # Вернись в главное меню или другое состояние
    # await manager.switch_to(MainMenu.menu)  # или manager.done() / manager.start(...)