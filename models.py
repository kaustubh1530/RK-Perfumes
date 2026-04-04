"""
models.py – Database Models
============================
Defines all SQLAlchemy ORM models used by RK Perfume.
"""

from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    """Tell Flask-Login how to reload a user from the session."""
    return Admin.query.get(int(user_id))


class Admin(UserMixin, db.Model):
    """
    Admin user who can log in to manage products.
    Only one admin account is needed for your sister.
    """
    __tablename__ = 'admin'

    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Admin {self.email}>'


class Perfume(db.Model):
    """
    A single perfume product sold on the website.
    All products are 'inspired-by' fragrances.
    """
    __tablename__ = 'perfume'

    id               = db.Column(db.Integer, primary_key=True)
    name             = db.Column(db.String(100), nullable=False)
    inspired_by      = db.Column(db.String(150), nullable=False)   # e.g. "Creed Aventus"
    description      = db.Column(db.Text, nullable=False)
    price            = db.Column(db.Float, nullable=False)
    quantity         = db.Column(db.Integer, default=0)
    category         = db.Column(db.String(50), default='Other')   # Floral / Woody / Fresh / Oriental
    image_filename   = db.Column(db.String(200), default='placeholder.svg')
    is_featured      = db.Column(db.Boolean, default=False)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def in_stock(self):
        return self.quantity > 0

    @property
    def stock_status(self):
        if self.quantity == 0:
            return 'out'
        if self.quantity <= 5:
            return 'low'
        return 'in'

    def __repr__(self):
        return f'<Perfume {self.name}>'