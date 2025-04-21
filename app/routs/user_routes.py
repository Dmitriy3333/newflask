from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.sanatorium import Sanatorium
from app.models.user import User
from app.models.user_preferences import UserPreferences
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
import json
from extensions import db

user_bp = Blueprint('user', __name__)
@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    # Проверка наличия пользователя в сессии
    if 'user_id' not in session:
        flash('Сначала войдите в аккаунт', 'warning')
        return redirect(url_for('user.login'))

    user = User.query.get(session['user_id'])

    # Если пользователя с таким id нет, возвращаем на страницу входа
    if user is None:
        flash('Пользователь не найден', 'danger')
        return redirect(url_for('user.login'))

    if request.method == 'POST':
        user_preferences = UserPreferences.query.filter_by(user_id=user.id).first()
        if not user_preferences:
            user_preferences = UserPreferences()
            user_preferences.user_id = user.id

        user_preferences.preferred_region = request.form.get('region') or 'Не указано'
        user_preferences.preferred_resort = request.form.get('resort') or 'Не указано'
        user_preferences.place_to_attractions = 'place_to_attractions' in request.form
        user_preferences.rating = request.form.get('rating', type=int) or 3
        user_preferences.treatmentbase = ','.join(request.form.getlist('treatment_base[]')) or 'Не указано'

        user_preferences.goal = request.form.get('purpose')
        user_preferences.budget = request.form.get('sum')
        user_preferences.preferred_country = request.form.get('country')
        user_preferences.sanatorium_type = request.form.get('type')

        services_list = request.form.getlist('services[]')
        user_preferences.services = ','.join(services_list) if services_list else None

        importance_factors = {
            'price': request.form.get('фактор_стоимости', type=int) or 3,
            'location': request.form.get('фактор_места', type=int) or 3,
            'treatment': request.form.get('фактор_базы', type=int) or 3,
            'living': request.form.get('фактор_условий', type=int) or 3,
            'entertainment': request.form.get('фактор_развлечений', type=int) or 3
        }
        user_preferences.importance_factors = json.dumps(importance_factors)

        db.session.add(user_preferences)
        db.session.commit()

        flash('Профиль успешно обновлён', 'success')
        return redirect(url_for('user.profile'))

    user_preferences = UserPreferences.query.filter_by(user_id=user.id).first()

    default_factors = {
        'price': 3,
        'location': 3,
        'treatment': 3,
        'living': 3,
        'entertainment': 3
    }

    if user_preferences and user_preferences.importance_factors:
        try:
            factors = json.loads(user_preferences.importance_factors)
            factors = {**default_factors, **factors}
        except json.JSONDecodeError:
            factors = default_factors
    else:
        factors = default_factors

    return render_template('profile.html', user=user, user_preferences=user_preferences, factors=factors)

@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = User()
        user.name = request.form['name']
        user.login = request.form['login']
        user.email = request.form['email']
        user.password = generate_password_hash(request.form['password'])
        user.is_admin = False
        db.session.add(user)
        db.session.commit()
        flash('Данные сохранены успешно!', 'success')
        return redirect(url_for('user.login'))

    return render_template("signup.html")

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        print(f"Login attempt: {login}, password: {password}")
        user = User.query.filter_by(login=login).first()
        print("User found:", user)

        if user:
            print("Stored password:", user.password)
            if check_password_hash(user.password, password):
                print("Password matches!")
                session['user_id'] = user.id
                session['user_name'] = user.name
                session['is_admin'] = user.is_admin
                flash('Вы успешно вошли!', 'success')
                return redirect(url_for('main.index'))
            else:
                print("Password mismatch!")
        else:
            print("User not found!")

        flash('Неверный логин или пароль', 'danger')

    return render_template("login.html")

@user_bp.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из аккаунта', 'info')
    return redirect(url_for('main.index'))