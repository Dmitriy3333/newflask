from app.routs import create_app
from extensions import db
from app.models.sanatorium import Sanatorium
from app.models.user_preferences import UserPreferences
from app.models.user import User
from flask import session


app = create_app()


user_id = 1  # пока тут будет просто фиксированный человек - его предпочтения, пока не знаю, как автоматически определять id авторизованного чела


with app.app_context(), app.test_request_context():

    session['user_id'] = user_id


    all_sanatoriums = Sanatorium.query.all()
    print(f"Вывод санаториев")
    for s in all_sanatoriums:
        print(f"{s.id}: {s.name}")

    user_id_from_session = session.get('user_id')  # тут тоже пока хз как получить реального чела

    if user_id_from_session:
        user = db.session.get(User, user_id_from_session)  # Ищем пользователя по user_id
        if user:
            print(f"User: {user.name}") #тут можно обращаться к элементам таблицы через ключи - можно посмотреть в models/


            preferences = UserPreferences.query.filter_by(user_id=user.id).first()
            if preferences:
                print(f"Бюджет: {preferences.budget}") #тут можно обращаться к элементам таблицы через ключи - можно посмотреть в models/
                print(f"Предпочтительный регион: {preferences.preferred_region}")
                print(f"Тип санатория: {preferences.sanatorium_type}")
                print(f"Услуги: {preferences.services}")

            else:
                print("Предпочтения не найдены")
        else:
            print("Пользователь не найден")
    else:
        print("Пользователь не авторизован")




