from config.config import Config, load_config
import aiohttp
import asyncio
from typing import List, Dict

config: Config = load_config()
URL = "https://app.chipp.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {config.ai.token}",
    "Content-Type": "application/json"
}


def _parse_diet_text(text):
    """
    Преобразует многострочный текст с суточными нормами в словарь:
    ключ - название показателя, значение - число (int или float).
    """
    result = {}

    lines = text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('Суточная норма:'):
            continue

        # Разделяем строку по двоеточию
        if ':' not in line:
            continue

        key_part, value_part = line.split(':', 1)
        key = key_part.strip()
        value_str = value_part.strip()

        # Убираем единицы измерения (ккал, г, мг и т.д.)
        # Оставляем только цифры, точку и минус (на всякий случай)
        cleaned_value = ''
        for char in value_str:
            if char.isdigit() or char == '.' or char == '-':
                cleaned_value += char
            elif char == ' ' and cleaned_value:  # пробелы между цифрами (например, 1 500)
                continue

        if cleaned_value:
            # Преобразуем в int, если возможно, иначе в float
            if '.' in cleaned_value:
                value = float(cleaned_value)
            else:
                value = int(cleaned_value)
            result[key] = value

    return result


async def get_day_diet(
    gender: str,
    age: int,
    height: int,
    weight: int,
    goal: str,
    activity: str,
    diet: list | str
) -> str:
    # Превращаем список диет в строку (или оставляем как есть)
    diet_str = ", ".join(diet) if isinstance(diet, list) else diet
    if not diet_str.strip():
        diet_str = "без ограничений"

    # Правильный формат сообщений для Chat Completions API
    messages: List[Dict[str, str]] = [
        {
            "role": "user",
            "content": "Ты — профессиональный спортивный диетолог и нутрициолог. "
                       "Отвечай строго по формату ниже, без лишних слов и символов."
                       f"Пол: {gender}\n"
                       f"Возраст: {age} лет\n"
                       f"Рост: {height} см\n"
                       f"Вес: {weight} кг\n"
                       f"Цель: {goal}\n"
                       f"Уровень активности: {activity}\n"
                       f"Специальная диета: {diet_str}\n\n"
                       "ВЫВЕДИ ТОЛЬКО СУТОЧНУЮ НОРМУ. НИКАКИХ ПОЯСНЕНИЙ И ПРИВЕТСТВИЙ.\n"
                       "Формат:\n"
                       "Суточная норма:\n"
                       "calories: ___ ккал\n"
                       "protein_grams: ___ г\n"
                       "fat_grams: ___ г\n"
                       "carbs_grams: ___ г\n"
                       "fiber_grams: ___ г\n"
                       "omega3_mg: ___ мг\n"
                       "potassium_mg: ___ мг\n"
                       "magnesium_mg: ___ мг\n"
                       "sodium_mg: ___ мг"
        }
    ]

    payload = {
        "model": "newapplication-61123",
        "messages": messages,
        "stream": False,
        "temperature": 0.3     # добавь для стабильности ответа
    }

    timeout = aiohttp.ClientTimeout(total=30)

    try:
        async with aiohttp.ClientSession(headers=HEADERS, timeout=timeout) as session:
            async with session.post(URL, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    content = data["choices"][0]["message"]["content"].strip()
                    nutrition_dict = _parse_diet_text(content)
                    return nutrition_dict
                else:
                    error = await resp.text()
                    print(f"API Error {resp.status}: {error}")
                    return f"Ошибка API: {resp.status}"
    except asyncio.TimeoutError:
        return "Таймаут запроса к Chipp.ai"
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return "Внутренняя ошибка сервера"

async def get_food_description(
    meal_description: str
) -> str:
    # Правильный формат сообщений для Chat Completions API
    messages: List[Dict[str, str]] = [
        {
            "role": "user",
            "content": "Ты — профессиональный спортивный диетолог и нутрициолог."
                        "Отвечай строго по формату ниже, без лишних слов и символов."
                        f"Анализируй следующий прием пищи: {meal_description}"
                        "ВЫВЕДИ ТОЛЬКО НУТРИЕНТЫ. НИКАКИХ ПОЯСНЕНИЙ И ПРИВЕТСТВИЙ."
                        "Формат:"
                        "calories: ___ ккал"
                        "protein_grams: ___ г"
                        "fat_grams: ___ г"
                        "carbs_grams: ___ г"
                        "fiber_grams: ___ г"
                        "omega3_mg: ___ мг"
                        "potassium_mg: ___ мг"
                        "magnesium_mg: ___ мг"
                        "sodium_mg: ___ мг"
        }
    ]

    payload = {
        "model": "newapplication-61123",
        "messages": messages,
        "stream": False,
        "temperature": 0.3     # добавь для стабильности ответа
    }

    timeout = aiohttp.ClientTimeout(total=30)

    try:
        async with aiohttp.ClientSession(headers=HEADERS, timeout=timeout) as session:
            async with session.post(URL, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    content = data["choices"][0]["message"]["content"].strip()
                    nutrition_dict = _parse_diet_text(content)
                    return nutrition_dict
                else:
                    error = await resp.text()
                    print(f"API Error {resp.status}: {error}")
                    return f"Ошибка API: {resp.status}"
    except asyncio.TimeoutError:
        return "Таймаут запроса к Chipp.ai"
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return "Внутренняя ошибка сервера"