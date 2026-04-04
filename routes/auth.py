"""
routes/auth.py – Authentication Routes
========================================
Handles admin login and logout.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import Admin
from extensions import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    """Show login form and process credentials."""
    # Already logged in → go straight to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        admin = Admin.query.filter_by(email=email).first()

        if admin and check_password_hash(admin.password_hash, password):
            login_user(admin, remember=False)
            flash('Welcome back! You are now logged in.', 'success')
            # Respect "next" param so Flask-Login redirects properly
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('admin/login.html')


@auth_bp.route('/admin/logout')
@login_required
def logout():
    """Log the admin out and redirect to login page."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))