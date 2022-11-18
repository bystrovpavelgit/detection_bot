"""models for SQLite"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.db import DB


class User(DB.Model, UserMixin):
    """User model"""
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(64), index=True, unique=True)
    password = DB.Column(DB.String(128))
    role = DB.Column(DB.String(10), index=True)

    @property
    def is_admin(self):
        """is admin"""
        return self.role == "admin"

    def __repr__(self):
        """repr method"""
        return "<User {} {}>".format(self.id, self.username)

    def set_password(self, password):
        """set password"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """check password"""
        return check_password_hash(self.password, password)


class Defects(DB.Model):
    """Defects model"""
    id = DB.Column(DB.Integer, primary_key=True)
    image = DB.Column(DB.String(128), nullable=True)
    object_class = DB.Column(DB.Integer, nullable=False)
    object_label = DB.Column(DB.String(64), nullable=False)

    def __repr__(self):
        """repr method"""
        return "<Defects {}>".format(self.id)


class CarCounts(DB.Model):
    """CarCounts model"""
    id = DB.Column(DB.Integer, primary_key=True)
    image = DB.Column(DB.String(128), nullable=True)
    car_count = DB.Column(DB.Integer, nullable=False)
    ratio = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        """repr method"""
        return "<CarCounts {}>".format(self.id)
