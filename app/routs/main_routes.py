from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.sanatorium import Sanatorium
from app.models.user import User
from app.models.user_preferences import UserPreferences
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
import json
from extensions import db
from app.models.sanatoriumPhoto import SanatoriumPhoto
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    sanatoriums = Sanatorium.query.all()

    photos_dict = {}
    for sanatorium in sanatoriums:
        photo = SanatoriumPhoto.query.filter_by(sanatorium_id=sanatorium.id).first()
        if photo:
            photos_dict[sanatorium.id] = photo.file_path

    return render_template('index.html', sanatoriums=sanatoriums, photos=photos_dict)

@main_bp.route('/about')
def about():
    return render_template("about.html")
