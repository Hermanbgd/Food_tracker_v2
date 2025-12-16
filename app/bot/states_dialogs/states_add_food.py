# Состояния добавления приема пищи
from aiogram.fsm.state import StatesGroup, State


class AddFood(StatesGroup):
    food_add = State()