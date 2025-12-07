from aiogram.fsm.state import StatesGroup, State


# состояния для заполнения профиля
class ProfileSetSG(StatesGroup):
    gender = State()
    age = State()
    height = State()
    weight = State()
    goal = State()
    activity = State()
    diet = State()