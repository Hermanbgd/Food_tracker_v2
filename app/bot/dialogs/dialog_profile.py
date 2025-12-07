from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, Button, Cancel, Back, Column, Multiselect
from aiogram_dialog.widgets.text import Const, Format

from app.bot.getters.getters_profile import get_diet_categories
from app.bot.handlers_dialogs.handlers_menu import go_profile
from app.bot.handlers_dialogs.handlers_profile import button_gender, handler_age, handler_height, \
    handler_weight, button_goal, button_activity, button_confirm_profile_set, cancel_to_main_profile
from app.bot.states_dialogs.states_profile import ProfileSetSG


create_profile = Dialog(
    # 1. Пол
    Window(
        Const('Создание профиля (1/7)\n\nТвой пол:'),
        Row(
            Button(Const('Мужской'), id='male', on_click=button_gender),
            Button(Const('Женский'), id='female', on_click=button_gender),
        ),
        Button(Const('Отмена'), id='cancel', on_click=cancel_to_main_profile),
        state=ProfileSetSG.gender,
    ),
    # 2. Возраст
    Window(
        Const("Создание профиля (2/7)\n\nСколько тебе лет?\nНапиши число от 14 до 80"),
        MessageInput(handler_age),
        Back(Const("Назад")),
        Button(Const('Отмена'), id='cancel', on_click=cancel_to_main_profile),
        state=ProfileSetSG.age,
    ),
    # 3. Рост
    Window(
        Const("Создание профиля (3/7)\n\nКакой твой рост в см?\nНапиши число от 100 до 250"),
        MessageInput(handler_height),
        Back(Const("Назад")),
        Button(Const('Отмена'), id='cancel', on_click=cancel_to_main_profile),
        state=ProfileSetSG.height,
    ),
    # 4. Вес
    Window(
        Const("Создание профиля (4/7)\n\nКакой твой текущий вес в кг?\nНапиши число от 30 до 200"),
        MessageInput(handler_weight),
        Back(Const("Назад")),
        Button(Const('Отмена'), id='cancel', on_click=cancel_to_main_profile),
        state=ProfileSetSG.weight,
    ),
    # 5. Цель
    Window(
        Const('Создание профиля (5/7)\n\nВыбери свою главную цель:'),
        Column(
            Button(Const('Похудеть'), id='lose', on_click=button_goal),
            Button(Const('Поддерживать вес'), id='hold', on_click=button_goal),
            Button(Const('Набрать массу'), id='gain', on_click=button_goal),
            Back(Const("Назад")),
        ),
        Button(Const('Отмена'), id='cancel', on_click=cancel_to_main_profile),
        state=ProfileSetSG.goal,
    ),
    # 6. Активность
    Window(
        Const('Создание профиля (6/7)\n\nУровень активности в обычной жизни:'),
        Column(
            Button(Const('Почти не двигаюсь'), id='sedentary', on_click=button_activity),
            Button(Const('Лёгкая'), id='light', on_click=button_activity),
            Button(Const('Средняя'), id='moderate', on_click=button_activity),
            Button(Const('Высокая'), id='active', on_click=button_activity),
            Back(Const("Назад")),
        ),
        Button(Const('Отмена'), id='cancel', on_click=cancel_to_main_profile),
        state=ProfileSetSG.activity,
    ),
    # 7. Диета
    Window(
        Const('Создание профиля (7/7)\n\nЕсть ли ограничения по питанию? (можно выбрать несколько):'),
        Column(
            Multiselect(
                checked_text=Format('✔️ {item[0]}'),
                unchecked_text=Format('⬜ {item[0]}'),
                id='diet_topics',
                item_id_getter=lambda x: str(x[1]),  # str для совместимости с list[str]
                items='categories',
                min_selected=1,
            ),
        ),
        Row(
            Back(Const("Назад")),
            Button(Const('Отмена'), id='cancel', on_click=cancel_to_main_profile),
        ),
        Button(Const('Подтвердить'),
               id='confirm',
               on_click=button_confirm_profile_set,
               when=lambda data, widget, manager: len(manager.find("diet_topics").get_checked()) > 0
               ),
        state=ProfileSetSG.diet,
        getter=get_diet_categories,
    ),
)