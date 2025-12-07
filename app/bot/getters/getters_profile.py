from aiogram_dialog import DialogManager

profile_data = "Профиль не заполнен!"

async def get_diet_categories(**kwargs):
    categories = [
        ('Нет', 1),
        ('Вегетарианец', 2),
        ('Веган', 3),
        ('Без лактозы', 4),
        ('Без глютена', 5),
    ]
    return {'categories': categories}
