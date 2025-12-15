from aiogram_dialog import DialogManager
from psycopg import AsyncConnection

from app.infrastructure.database.db import get_user_profile, get_user_nutrition_limit


async def diet_info(dialog_manager: DialogManager, **kwargs):
    # получаем соединение conn из миддлвари
    conn: AsyncConnection = kwargs["conn"]
    # Получаем ID пользователя безопасно
    user_id = dialog_manager.event.from_user.id  # правильнее и короче

    # Правильно вызываем асинхронную функцию
    info_diet = await get_user_nutrition_limit(conn, user_id=user_id)

    if info_diet is None:
        diet_data = "Профиль не заполнен"
    else:
        # Если красивый вывод, то распаковать
        calories, protein_grams, fat_grams, carbs_grams, fiber_grams, omega3_mg, potassium_mg, magnesium_mg, sodium_mg, = info_diet
        diet_data = (
            f"📊 Твой персональный план питания:\n\n"
            f"🔥 Суточная норма калорий: {calories} ккал\n"
            f"💪 Белки: {protein_grams} г\n"
            f"🧈 Жиры: {fat_grams} г\n"
            f"🌾 Углеводы: {carbs_grams} г\n"
            f"🥬 Клетчатка: {fiber_grams} г\n"
            f"🐟 Омега-3: {omega3_mg} мг\n"
            f"🍌 Калий: {potassium_mg} мг\n"
            f"🥜 Магний: {magnesium_mg} мг\n"
            f"🧂 Натрий: {sodium_mg} мг\n\n"
            f"Всё рассчитано именно под тебя — держи курс и будет результат! 🚀💚"
        )

    return {"diet_info": diet_data}