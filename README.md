python3 << 'PYEOF'
readme = """# RK Perfume — Full-Stack E-Commerce Web Application

A complete, production-ready e-commerce website built for a perfume business selling inspired-by fragrances. Built from scratch with Python Flask, PostgreSQL, and deployed on Railway.

![RK Perfume](https://web-production-a5af4.up.railway.app)

## Live Demo
🔗 [https://web-production-a5af4.up.railway.app](https://web-production-a5af4.up.railway.app)

---

## Features

### Customer Facing
- Home page with featured perfumes and hero section
- Product listing with search and category filter
- Individual product detail pages with inspired-by information
- WhatsApp ordering integration
- Contact page with enquiry form
- Complete policy pages (Privacy, Terms, Shipping, Returns)
- 📱 Fully responsive design for mobile and desktop

### Admin Panel
- Secure login with password hashing
- Add new perfumes with image upload
- Edit existing perfumes (price, stock, description, image)
- Delete perfumes
- Feature products on home page
- Stock management dashboard

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Database | PostgreSQL (Railway) |
| ORM | SQLAlchemy |
| Authentication | Flask-Login |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Image Storage | Cloudinary |
| Deployment | Railway |
| Version Control | Git, GitHub |
| Web Server | Gunicorn |

---

## Project Structure

RK_perfume-shop/
├── app.py                  # Flask app entry point
├── models.py               # Database models
├── extensions.py           # Flask extensions
├── requirements.txt        # Python dependencies
├── Procfile               # Railway deployment config
├── routes/
│   ├── auth.py            # Login/logout
│   ├── products.py        # Public pages
│   └── admin.py           # Admin CRUD + Cloudinary
├── templates/
│   ├── base.html          # Shared layout
│   ├── index.html         # Home page
│   ├── shop.html          # Product listing
│   ├── product_detail.html # Product detail
│   ├── contact.html       # Contact page
│   ├── privacy.html       # Privacy policy
│   ├── terms.html         # Terms & conditions
│   ├── shipping.html      # Shipping policy
│   ├── returns.html       # Returns policy
│   └── admin/
│       ├── login.html     # Admin login
│       ├── dashboard.html # Product management
│       └── add_edit.html  # Add/edit form
└── static/
├── css/
│   ├── style.css      # Main styles
│   └── admin.css      # Admin styles
├── js/main.js         # JavaScript
└── images/            # Static images

---

## Run Locally

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/kaustubh1530/RK-Perfumes.git
cd RK-Perfumes

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\\Scripts\\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
echo "SECRET_KEY=your-secret-key-here" > .env

# 5. Run the app
python app.py
```

Visit: `http://127.0.0.1:5000`

---

## Admin Access

| Field | Value |
|-------|-------|
| URL | `/admin/login` |
| Email | `admin@rkperfume.com` |
| Password | Set via environment |

---

# Deployment (Railway)

1. Push code to GitHub
2. Connect repo to Railway
3. Add environment variables:
   - `SECRET_KEY`
   - `DATABASE_URL` (PostgreSQL)
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`
4. Deploy automatically on every git push

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask secret key for sessions |
| `DATABASE_URL` | PostgreSQL connection URL |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret |

---

## Developer

**Kaustubh Patil**
- GitHub: [@kaustubh1530](https://github.com/kaustubh1530)
- University of the Potomac — BS Computer Science (Software Engineering)

---

## License

This project is for portfolio and demonstration purposes.

---

*All perfumes are inspired-by recreations. Trademarks belong to their respective owners.*


👨‍💻 Developer

Kaustubh Patil
- GitHub: @kaustubh1530
- LinkedIn: linkedin.com/in/kaustubh-patil1530
- Email: kauspatil1530@gmail.com
- University of the Potomac — BS Computer Science

"""