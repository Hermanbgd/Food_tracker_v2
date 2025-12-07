from aiogram_dialog import DialogManager
from psycopg import AsyncConnection

from app.infrastructure.database.db import get_user_profile


async def profile_info(dialog_manager: DialogManager, **kwargs):
    # получаем соединение conn из миддлвари
    conn: AsyncConnection = kwargs["conn"]
    # Получаем ID пользователя безопасно
    user_id = dialog_manager.event.from_user.id  # правильнее и короче

    # Правильно вызываем асинхронную функцию
    info_prof = await get_user_profile(conn, user_id=user_id)

    if info_prof is None:
        profile_data = "Профиль не заполнен"
    else:
        # Если красивый вывод, то распаковать
        gender, age, height, weight, goal, activity, diet = info_prof
        profile_data = (
            f"Пол: {gender}\n"
            f"Возраст: {age}\n"
            f"Рост: {height} см\n"
            f"Вес: {weight} кг\n"
            f"Цель: {goal}\n"
            f"Активность: {activity}\n"
            f"Питание: {diet}"
        )

    return {"profile_info": profile_data}