from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from app.models.sanatorium import Sanatorium
from app.models.sanatoriumPhoto import SanatoriumPhoto
from app.models.user import User

import os
from werkzeug.utils import secure_filename

sanatoriums_bp = Blueprint('sanatoriums', __name__)
UPLOAD_FOLDER = 'static/uploads'

@sanatoriums_bp.route('/create', methods=['GET', 'POST'])
@sanatoriums_bp.route('/create/<int:id>', methods=['GET', 'POST'])
def create(id=None):
    sanatorium = Sanatorium.query.get(id) if id else None

    if request.method == 'POST':
        # Удаляем фото, отмеченные на удаление
        delete_ids = request.form.getlist('delete_photos')
        for photo_id in delete_ids:
            photo = SanatoriumPhoto.query.get(int(photo_id))
            if photo and (not sanatorium or photo.sanatorium_id == sanatorium.id):
                try:
                    # Удаляем файл с диска
                    full_path = os.path.join('static', photo.file_path)
                    if os.path.exists(full_path):
                        os.remove(full_path)
                except Exception as e:
                    print(f"Ошибка при удалении файла {photo.file_path}: {e}")

                db.session.delete(photo)
        ############
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        photos = request.files.getlist('photos')
        if len(photos) > 10:
            flash('Максимум 10 фото можно загрузить', 'warning')
            return redirect(url_for('sanatoriums.create', id=id if id else ''))
        ############
        try:
            if not sanatorium:
                sanatorium = Sanatorium()
                db.session.add(sanatorium)

            # Обновляем поля
            sanatorium.has_pool = 'has_pool' in request.form
            sanatorium.has_spa = 'has_spa' in request.form
            sanatorium.has_entertainment = 'has_entertainment' in request.form
            sanatorium.has_sports_facilities = 'has_sports_facilities' in request.form

            sanatorium.specialization = ', '.join(request.form.getlist('specialization[]')) or None
            sanatorium.equipment = ', '.join(request.form.getlist('equipment[]')) or None
            sanatorium.room_types = ', '.join(request.form.getlist('room_types[]')) or None
            sanatorium.amenities = ', '.join(request.form.getlist('amenities[]')) or None

            sanatorium.name = request.form['name']
            sanatorium.description = request.form.get('description')
            sanatorium.website = request.form.get('website')
            sanatorium.price_per_night = float(request.form['price_per_night'])
            sanatorium.price_per_service = float(request.form.get('price_per_service', 0))
            sanatorium.country = request.form['country']
            sanatorium.region = request.form['region']
            sanatorium.resort = request.form['resort']
            sanatorium.place_to_attractions = int(request.form['place_to_attractions'])
            sanatorium.food_type = request.form['food_type']
            sanatorium.food_quality = int(request.form.get('food_quality', 0))
            sanatorium.average_review_score = float(request.form.get('average_review_score', 0))
            sanatorium.phone = request.form.get('phone')
            sanatorium.email = request.form.get('email')

            db.session.flush()  # Сохраняем sanatorium.id до коммита

            #####################
            # Сохраняем фото
            for photo in photos:
                if photo and photo.filename:
                    filename = secure_filename(photo.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    photo.save(filepath)

                    # Сохраняем путь относительно static/
                    relative_path = os.path.relpath(filepath, 'static')

                    photo_record = SanatoriumPhoto(
                        sanatorium_id=sanatorium.id,
                        file_path=relative_path
                    )
                    db.session.add(photo_record)
            ##################

            db.session.commit()
            flash('Данные и фотографии сохранены успешно!', 'success')
            return redirect(url_for('main.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при сохранении: {str(e)}', 'danger')
            return redirect(url_for('sanatoriums.create', id=id if id else ''))

    return render_template('create.html',
                           sanatorium=sanatorium or Sanatorium(),
                           photos=sanatorium.photos if sanatorium else [])
@sanatoriums_bp.route('/sanatorium/<int:id>')
def sanatorium(id):
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])

    sanatorium = Sanatorium.query.get_or_404(id)

    return render_template("sanatorium.html", sanatorium=sanatorium, user=user)

@sanatoriums_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    sanatorium = Sanatorium.query.get_or_404(id)
    db.session.delete(sanatorium)
    db.session.commit()
    flash('Санаторий удалён', 'success')
    return redirect(url_for('main.index'))
