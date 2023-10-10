from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('app.config')
Session(app)
CORS(app, supports_credentials=True)

db = SQLAlchemy(app)

from app import endpoints

with app.app_context():
    db.create_all()
