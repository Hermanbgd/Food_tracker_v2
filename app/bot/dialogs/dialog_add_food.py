from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Column, Button, Back
from aiogram_dialog.widgets.text import Const, Format

from app.bot.states_dialogs.states_add_food import AddFood

add_food = Dialog(
    Window(
        Const('Запиши голосовое или текстовое сообщение, расскажи что ты съел.'),
        state=AddFood.food_add,
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
)