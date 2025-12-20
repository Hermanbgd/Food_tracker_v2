# Главное меню
from aiogram.enums import ContentType
from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, Button, Cancel, Back, Column, Multiselect
from aiogram_dialog.widgets.text import Const, Format

from app.bot.getters.getters_menu import diet_info
from app.bot.handlers_dialogs.handlers_menu import add_food, go_profile, set_profile, view_food, go_main_menu, \
    handle_food_input
from app.bot.handlers_dialogs.handlers_profile import cancel_to_main_profile
from app.bot.states_dialogs.states_menu import MainMenu

main_menu = Dialog(
    Window(
        Const('🏠 Главное меню\n\nАI-трекер калорий всегда на страже качества твоего питания. Чем могу помочь?'),
        Column(
            Button(Const('📸 Добавить прием пищи'), id='add_food', on_click=add_food),
            Button(Const('👤 Мой профиль'), id='my_profile', on_click=go_profile),
        ),
        state=MainMenu.menu,
    ),
    Window(
        Format('{diet_info}'),
        Column(
        Button(Const('Заполнить профиль'), id='profile_set', on_click=set_profile),
            Button(Const('🥗 Приемы пищи'), id='add_food', on_click=view_food),
            Back(Const('Главное меню')),
        ),
        getter=diet_info,
        state=MainMenu.profile,
    ),
    Window(
        Const('Запиши голосовое или текстовое сообщение, расскажи что ты съел.'),
        # MessageInput(handle_food_input, content_types=[ContentType.TEXT, ContentType.VOICE]),
        MessageInput(handle_food_input),
        Column(
            Button(Const('Главное меню'), id='m_menu', on_click=go_main_menu),
        ),
        state=MainMenu.food_add,
    ),
)