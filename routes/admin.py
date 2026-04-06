"""
routes/admin.py - Admin Panel Routes
All routes protected by @login_required.
Images stored on Cloudinary for permanent storage.
"""

import os
import cloudinary
import cloudinary.uploader
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from models import Perfume
from extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME", "dh6bpudsk"),
    api_key=os.environ.get("CLOUDINARY_API_KEY", "233827859241376"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET", "pCdeDPR8MZg7AOlXRE4VxXarhvA")
)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file):
    """Upload image to Cloudinary. Returns URL string or None."""
    if not file or not file.filename:
        return None
    if not allowed_file(file.filename):
        flash("Invalid file type. Use JPG, PNG, WebP or GIF.", "danger")
        return None
    try:
        result = cloudinary.uploader.upload(
            file,
            folder="rk_perfume",
            transformation=[{"width": 600, "height": 720, "crop": "fill", "quality": "auto"}]
        )
        print("Image uploaded to Cloudinary: " + result["secure_url"])
        return result["secure_url"]
    except Exception as e:
        print("Cloudinary upload error: " + str(e))
        flash("Image upload failed. Please try again.", "danger")
        return None


# Dashboard
@admin_bp.route("/")
@login_required
def dashboard():
    perfumes     = Perfume.query.order_by(Perfume.name).all()
    total        = len(perfumes)
    low_stock    = sum(1 for p in perfumes if p.stock_status == "low")
    out_of_stock = sum(1 for p in perfumes if p.stock_status == "out")
    return render_template(
        "admin/dashboard.html",
        perfumes=perfumes,
        total=total,
        low_stock=low_stock,
        out_of_stock=out_of_stock
    )


# Add Perfume
@admin_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_perfume():
    if request.method == "POST":
        name        = request.form.get("name", "").strip()
        inspired_by = request.form.get("inspired_by", "").strip()
        description = request.form.get("description", "").strip()
        category    = request.form.get("category", "Other").strip()
        is_featured = "is_featured" in request.form

        try:
            price    = float(request.form.get("price", 0))
            quantity = int(request.form.get("quantity", 0))
        except ValueError:
            flash("Price and quantity must be valid numbers.", "danger")
            return redirect(url_for("admin.add_perfume"))

        if not name or not inspired_by or not description:
            flash("Name, Inspired By, and Description are required.", "danger")
            return redirect(url_for("admin.add_perfume"))

        image_url = save_image(request.files.get("image"))
        if not image_url:
            image_url = "placeholder.png"

        perfume = Perfume(
            name=name, inspired_by=inspired_by, description=description,
            price=price, quantity=quantity, category=category,
            image_filename=image_url, is_featured=is_featured
        )
        db.session.add(perfume)
        db.session.commit()
        flash(f"{name} added successfully!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/add_edit.html", perfume=None, action="Add")


# Edit Perfume
@admin_bp.route("/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_perfume(product_id):
    perfume = Perfume.query.get_or_404(product_id)

    if request.method == "POST":
        perfume.name        = request.form.get("name", "").strip()
        perfume.inspired_by = request.form.get("inspired_by", "").strip()
        perfume.description = request.form.get("description", "").strip()
        perfume.category    = request.form.get("category", "Other").strip()
        perfume.is_featured = "is_featured" in request.form

        try:
            perfume.price    = float(request.form.get("price", perfume.price))
            perfume.quantity = int(request.form.get("quantity", perfume.quantity))
        except ValueError:
            flash("Price and quantity must be valid numbers.", "danger")
            return redirect(url_for("admin.edit_perfume", product_id=product_id))

        new_image = save_image(request.files.get("image"))
        if new_image:
            perfume.image_filename = new_image

        db.session.commit()
        flash(f"{perfume.name} updated successfully!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/add_edit.html", perfume=perfume, action="Edit")


# Delete Perfume
@admin_bp.route("/delete/<int:product_id>", methods=["POST"])
@login_required
def delete_perfume(product_id):
    perfume = Perfume.query.get_or_404(product_id)
    name = perfume.name
    db.session.delete(perfume)
    db.session.commit()
    flash(f"{name} deleted.", "info")
    return redirect(url_for("admin.dashboard"))


# Toggle Featured
@admin_bp.route("/toggle-featured/<int:product_id>", methods=["POST"])
@login_required
def toggle_featured(product_id):
    perfume = Perfume.query.get_or_404(product_id)
    perfume.is_featured = not perfume.is_featured
    db.session.commit()
    status = "featured" if perfume.is_featured else "unfeatured"
    flash(f"{perfume.name} is now {status}.", "success")
    return redirect(url_for("admin.dashboard"))
