# Состояния главного меню
from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    menu = State()
    profile = State()
    food_add = State()