from database import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_diet = db.Column(db.Boolean, nullable=False)
    is_diet = db.Column(db.Boolean, nullable=False)