from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from psycopg import AsyncConnection

from app.bot.states_dialogs.states_menu import MainMenu
from app.infrastructure.database.db import add_user_profile

# Обработчики кнопок (добавил await callback.answer() везде)
async def button_gender(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    gender = button.widget_id
    dialog_manager.dialog_data["gender"] = gender
    await callback.answer()
    await dialog_manager.next()


async def button_goal(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    goal = button.widget_id
    dialog_manager.dialog_data["goal"] = goal
    await callback.answer()
    await dialog_manager.next()


async def button_activity(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    activity = button.widget_id
    dialog_manager.dialog_data["activity"] = activity
    await callback.answer()
    await dialog_manager.next()

async def cancel_to_main_profile(callback: CallbackQuery, button: Button, manager: DialogManager):
    # Полностью сбрасываем стек и переходим в нужное состояние другого SG
    await manager.start(MainMenu.profile, mode=StartMode.RESET_STACK)


async def button_confirm_profile_set(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    conn = dialog_manager.middleware_data["conn"]
    user_id = dialog_manager.event.from_user.id

    selected_ids = dialog_manager.find("diet_topics").get_checked()
    ALL_CATEGORIES = [('Нет', 1), ('Вегетарианец', 2), ('Веган', 3), ('Без лактозы', 4), ('Без глютена', 5)]
    selected_names = [name for name, cat_id in ALL_CATEGORIES if str(cat_id) in selected_ids]
    if 'Нет' in selected_names and len(selected_names) > 1:
        selected_names = ['Нет']

    dialog_manager.dialog_data["diet"] = selected_names

    # Записываем в БД
    await add_user_profile(
        conn,
        user_id=user_id,
        gender=dialog_manager.dialog_data["gender"],
        age=dialog_manager.dialog_data["age"],
        height=dialog_manager.dialog_data["height"],
        weight=dialog_manager.dialog_data["weight"],
        goal=dialog_manager.dialog_data["goal"],
        activity=dialog_manager.dialog_data["activity"],
        diet=selected_names
    )

    # сначала переключаем состояние!
    await dialog_manager.start(MainMenu.profile, mode=StartMode.RESET_STACK)

    # Теперь можно ответить, ответ придёт в новом окне
    await callback.answer("Профиль успешно сохранён!", show_alert=True)



# Обработчики ввода чисел (try-except для delete + ShowMode)
async def handler_age(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    try:
        age = int(message.text.strip())
        if 14 <= age <= 80:
            dialog_manager.dialog_data["age"] = age
            try:
                await message.delete()
            except Exception:
                pass
            await dialog_manager.next()
            return
    except ValueError:
        pass


async def handler_height(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    try:
        height = int(message.text.strip())
        if 100 <= height <= 250:
            dialog_manager.dialog_data["height"] = height
            try:
                await message.delete()
            except Exception:
                pass
            await dialog_manager.next()
            return
    except ValueError:
        pass


async def handler_weight(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    try:
        weight = int(message.text.strip())
        if 30 <= weight <= 200:
            dialog_manager.dialog_data["weight"] = weight
            try:
                await message.delete()
            except Exception:
                pass
            await dialog_manager.next()
            return
    except ValueError:
        pass