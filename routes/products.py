"""
routes/products.py – Public-Facing Product Routes
===================================================
Home page, product listing, product detail, contact.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Perfume

products_bp = Blueprint('products', __name__)


@products_bp.route('/')
def home():
    """Home page – show 3 featured perfumes plus latest arrivals."""
    featured = Perfume.query.filter_by(is_featured=True).limit(3).all()
    # Fall back to newest products if none are marked featured
    if not featured:
        featured = Perfume.query.order_by(Perfume.created_at.desc()).limit(3).all()
    return render_template('index.html', featured=featured)


@products_bp.route('/shop')
def shop():
    """Product listing page with optional search and category filter."""
    query    = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()

    perfumes = Perfume.query

    if query:
        like = f'%{query}%'
        perfumes = perfumes.filter(
            Perfume.name.ilike(like) |
            Perfume.inspired_by.ilike(like) |
            Perfume.description.ilike(like)
        )

    if category:
        perfumes = perfumes.filter_by(category=category)

    perfumes = perfumes.order_by(Perfume.name).all()

    # Unique categories for the filter bar
    all_categories = [r[0] for r in Perfume.query.with_entities(Perfume.category).distinct().all()]

    return render_template(
        'shop.html',
        perfumes=perfumes,
        categories=all_categories,
        current_q=query,
        current_cat=category
    )


@products_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """Individual product detail page."""
    perfume = Perfume.query.get_or_404(product_id)
    # Suggest 3 related products from the same category
    related = (
        Perfume.query
        .filter(Perfume.category == perfume.category, Perfume.id != perfume.id)
        .limit(3).all()
    )
    return render_template('product_detail.html', perfume=perfume, related=related)


@products_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page – form submission shows a success message."""
    if request.method == 'POST':
        name    = request.form.get('name', '').strip()
        email   = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            flash('Please fill in all fields.', 'danger')
        else:
            # In production: send email via Flask-Mail or save to DB
            flash(f'Thank you, {name}! We\'ll be in touch soon.', 'success')
            return redirect(url_for('products.contact'))

    return render_template('contact.html')

@products_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")

@products_bp.route("/terms")
def terms():
    return render_template("terms.html")

@products_bp.route("/shipping")
def shipping():
    return render_template("shipping.html")

@products_bp.route("/returns")
def returns():
    return render_template("returns.html")
