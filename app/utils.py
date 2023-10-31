import os
from functools import wraps

from flask import jsonify, current_app, url_for
from flask import session as flask_session
from werkzeug.utils import secure_filename

from app import app
from app.storages import User


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not flask_session.get("user_id"):
            return jsonify({"message": "Требуется авторизация"}), 401
        return func(*args, **kwargs)

    return decorated_function


def safe_convert(value):
    try:
        if value is None or value == "null":
            return None
        return value
    except (ValueError, TypeError):
        return None


def get_full_name():
    user_id = flask_session.get("user_id")

    if user_id is not None:
        user_data = User.query.filter_by(id=user_id).first()
        if user_data:
            user_name = user_data.user_name
            return user_name
        else:
            return jsonify({'message': 'Пользователь не найден'}), 404
    else:
        return jsonify({'message': 'Пользователь не аутентифицирован'}), 401


def save_file(file_field):
    if file_field:
        filename = secure_filename(file_field.filename)
        file_path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'], filename)
        file_field.save(file_path)
        file_url = url_for('uploaded_file', filename=filename, _external=True)
        return file_url
    else:
        return None