import os
import secrets
from dotenv import load_dotenv
load_dotenv()
"""
app.py  —  RK Perfume
======================
Uses the Application Factory pattern to avoid circular imports.
All extensions live in extensions.py and are bound to the app here.
"""

from flask import Flask
from extensions import db, login_manager          # ← from extensions, not circular


def create_app():
    app = Flask(__name__)

    # ── Config ────────────────────────────────────────────────
    app.config['SECRET_KEY']                     = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    db_url = os.environ.get('DATABASE_URL', 'sqlite:///rk_perfume.db')
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER']                  = os.path.join('static', 'images')
    app.config['MAX_CONTENT_LENGTH']             = 8 * 1024 * 1024   # 8 MB

    # ── Bind extensions ───────────────────────────────────────
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view             = 'auth.login'
    login_manager.login_message          = 'Please log in to access the admin panel.'
    login_manager.login_message_category = 'warning'

    # ── Register blueprints ───────────────────────────────────
    from routes.auth     import auth_bp
    from routes.products import products_bp
    from routes.admin    import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(admin_bp)

    return app


def seed_data():
    """Insert default admin + sample perfumes on first run."""
    from models import Admin, Perfume
    from werkzeug.security import generate_password_hash

    if not Admin.query.first():
        admin = Admin(
            email='admin@rkperfume.com',
            password_hash=generate_password_hash('Admin@1234')
        )
        db.session.add(admin)
        db.session.commit()
        print("✅  Default admin created  →  admin@rkperfume.com / Admin@1234")

    if not Perfume.query.first():
        samples = [
            Perfume(
                name='RK Cactus Garden',
                inspired_by='Louis Vuitton – Cactus Garden',
                description=(
                    'A bold, woody aromatic inspired by Louis Vuitton\'s Cactus Garden. '
                    'Opens with crisp cactus and green fig, blossoming into earthy vetiver '
                    'and cedarwood. A statement scent for the adventurous spirit.'
                ),
                price=35.00, quantity=20, category='Woody',
                image_filename='placeholder.svg', is_featured=True
            ),
            Perfume(
                name='RK Aventus',
                inspired_by='Creed – Aventus',
                description=(
                    'Our tribute to the legendary Creed Aventus. Bright pineapple and '
                    'blackcurrant open to a smoky birch and oakmoss heart, drying down to '
                    'ambergris and musk. Confidence in every spray.'
                ),
                price=45.00, quantity=15, category='Chypre',
                image_filename='placeholder.svg', is_featured=True
            ),
            Perfume(
                name='RK Aventus Cologne',
                inspired_by='Creed – Aventus Cologne',
                description=(
                    'Inspired by Creed\'s Aventus Cologne — a fresher, aquatic take on the '
                    'Aventus lineage. Icy mint and pink pepper burst over a clean woody base '
                    'of sandalwood and white musk. Effortlessly elegant.'
                ),
                price=40.00, quantity=18, category='Fresh',
                image_filename='placeholder.svg', is_featured=True
            ),
            Perfume(
                name='RK Black Phantom',
                inspired_by='Kilian – Black Phantom',
                description=(
                    'Inspired by Kilian\'s Black Phantom. Dark rum and black sugar envelop '
                    'a smoky coffee heart, anchored by sandalwood and vanilla. '
                    'Seductive, dramatic, unforgettable.'
                ),
                price=42.00, quantity=10, category='Oriental',
                image_filename='placeholder.svg'
            ),
            Perfume(
                name='RK Baccarat Rouge',
                inspired_by='Maison Francis Kurkdjian – Baccarat Rouge 540',
                description=(
                    'Our homage to the iconic Baccarat Rouge 540. Jasmine and saffron '
                    'shimmer above a luminous ambergris and cedarwood base. Weightless, '
                    'radiant, and impossibly addictive.'
                ),
                price=48.00, quantity=12, category='Floral',
                image_filename='placeholder.svg'
            ),
            Perfume(
                name='RK Oud Wood',
                inspired_by='Tom Ford – Oud Wood',
                description=(
                    'Inspired by Tom Ford\'s Oud Wood. Rare oud wood is softened by '
                    'rosewood and cardamom, then warmed by sandalwood, vetiver and amber. '
                    'Rich, smoky and effortlessly sophisticated.'
                ),
                price=38.00, quantity=25, category='Woody',
                image_filename='placeholder.svg'
            ),
        ]
        db.session.bulk_save_objects(samples)
        db.session.commit()
        print("✅  6 sample perfumes added.")


# ── Create app instance (needed by Flask's dev server) ────────
app = create_app()

# ── Auto-create database tables on startup (needed for Railway) ─
with app.app_context():
    from extensions import db
    from models import Admin, Perfume
    db.create_all()
    # Seed data if empty
    from werkzeug.security import generate_password_hash
    if not Admin.query.first():
        admin = Admin(
            email="admin@rkperfume.com",
            password_hash=generate_password_hash("Admin@1234")
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created")
    if not Perfume.query.first():
        samples = [
            Perfume(name="RK Cactus Garden", inspired_by="Louis Vuitton - Cactus Garden", description="A bold woody aromatic inspired by Louis Vuitton Cactus Garden. Opens with crisp cactus and green fig.", price=35.00, quantity=20, category="Woody", image_filename="placeholder.png", is_featured=True),
            Perfume(name="RK Aventus", inspired_by="Creed - Aventus", description="Our tribute to the legendary Creed Aventus. Bright pineapple and blackcurrant open to a smoky birch heart.", price=45.00, quantity=15, category="Chypre", image_filename="placeholder.png", is_featured=True),
            Perfume(name="RK Aventus Cologne", inspired_by="Creed - Aventus Cologne", description="Inspired by Creed Aventus Cologne. Icy mint and pink pepper burst over a clean woody base.", price=40.00, quantity=18, category="Fresh", image_filename="placeholder.png", is_featured=True),
            Perfume(name="RK Black Phantom", inspired_by="Kilian - Black Phantom", description="Inspired by Kilian Black Phantom. Dark rum and black sugar envelop a smoky coffee heart.", price=42.00, quantity=10, category="Oriental", image_filename="placeholder.png"),
            Perfume(name="RK Baccarat Rouge", inspired_by="Maison Francis Kurkdjian - Baccarat Rouge 540", description="Our homage to Baccarat Rouge 540. Jasmine and saffron shimmer above a luminous ambergris base.", price=48.00, quantity=12, category="Floral", image_filename="placeholder.png"),
            Perfume(name="RK Oud Wood", inspired_by="Tom Ford - Oud Wood", description="Inspired by Tom Ford Oud Wood. Rare oud wood softened by rosewood and cardamom.", price=38.00, quantity=25, category="Woody", image_filename="placeholder.png"),
        ]
        db.session.bulk_save_objects(samples)
        db.session.commit()
        print("Sample perfumes added")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True, port=5000)
@app.route('/init-db-now')
def init_db_now():
    from models import Admin, Perfume
    from werkzeug.security import generate_password_hash
    from extensions import db
    db.create_all()
    if not Admin.query.first():
        admin = Admin(email='admin@rkperfume.com', password_hash=generate_password_hash('RKPerfume@2025'))
        db.session.add(admin)
    if not Perfume.query.first():
        samples = [
            Perfume(name='RK Cactus Garden', inspired_by='Louis Vuitton - Cactus Garden', description='A bold woody aromatic inspired by Louis Vuitton Cactus Garden. Opens with crisp cactus and green fig.', price=2999, quantity=20, category='Woody', image_filename='placeholder.png', is_featured=True),
            Perfume(name='RK Aventus', inspired_by='Creed - Aventus', description='Our tribute to the legendary Creed Aventus. Bright pineapple and blackcurrant open to a smoky birch heart.', price=3999, quantity=15, category='Chypre', image_filename='placeholder.png', is_featured=True),
            Perfume(name='RK Aventus Cologne', inspired_by='Creed - Aventus Cologne', description='Inspired by Creed Aventus Cologne. Fresh icy mint and pink pepper.', price=3499, quantity=18, category='Fresh', image_filename='placeholder.png', is_featured=True),
            Perfume(name='RK Black Phantom', inspired_by='Kilian - Black Phantom', description='Inspired by Kilian Black Phantom. Dark rum and black sugar.', price=3699, quantity=10, category='Oriental', image_filename='placeholder.png'),
            Perfume(name='RK Baccarat Rouge', inspired_by='MFK - Baccarat Rouge 540', description='Our homage to Baccarat Rouge 540. Jasmine and saffron shimmer above luminous ambergris.', price=4299, quantity=12, category='Floral', image_filename='placeholder.png'),
            Perfume(name='RK Oud Wood', inspired_by='Tom Ford - Oud Wood', description='Inspired by Tom Ford Oud Wood. Rare oud wood softened by rosewood and cardamom.', price=3299, quantity=25, category='Woody', image_filename='placeholder.png'),
        ]
        db.session.bulk_save_objects(samples)
        db.session.commit()
    return 'Done! Database ready. Visit /admin/login now!'
