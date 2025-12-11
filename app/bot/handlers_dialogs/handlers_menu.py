from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from app.bot.states_dialogs.states_menu import MainMenu
from app.bot.states_dialogs.states_profile import ProfileSetSG


async def add_food(callback:CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.answer()

async def view_food(callback: CallbackQuery, button:Button, dialog_manager: DialogManager):
    await callback.answer()


async def go_profile(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=MainMenu.profile)

async def set_profile(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=ProfileSetSG.gender, mode=StartMode.RESET_STACK)

# async def go_main_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
#     await dialog_manager.start(state=MainMenu.menu, mode=StartMode.RESET_STACK)