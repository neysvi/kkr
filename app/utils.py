from functools import wraps

from flask import jsonify, request
from flask import session as flask_session


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print(request.cookies.get("session"))
        if not flask_session.get("user_id"):
            return jsonify({"message": "Требуется авторизация"}), 401
        return func(*args, **kwargs)

    return decorated_function
