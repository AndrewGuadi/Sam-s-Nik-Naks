# app/blueprints/main/routes.py
from flask import Blueprint, render_template, render_template_string, request, jsonify, redirect, url_for
from . import main

# ---------- Shared demo data ----------
def _demo_drop():
    return {
        "title": "Retro Keycaps",
        "subtitle": "Small batch, limited restock.",
        "image": "img/hero.jpg",
        "badge": "New",
    }

def _demo_products():
    return [
        {"id": 1, "slug": "sticker-pack", "name": "Sticker Pack", "short": "5 pack", "price": 9.99, "image": "img/prod1.jpg"},
        {"id": 2, "slug": "pin-cat", "name": "Enamel Pin", "short": "Cat edition", "price": 12.00, "image": "img/prod2.jpg"},
        {"id": 3, "slug": "keychain", "name": "Keychain", "short": "Acrylic", "price": 7.50, "image": "img/prod3.jpg"},
        {"id": 4, "slug": "mystery", "name": "Mystery Nik Nak", "short": "Limited", "price": 6.00, "image": "img/prod4.jpg"},
    ]

def _demo_reviews():
    return [
        {"name": "Alex R.", "text": "Fast shipping and great packaging", "location": "PA"},
        {"name": "Sam K.", "text": "The drop sold out quick. Love the pin", "location": "NJ"},
        {"name": "Dana P.", "text": "Exactly as pictured. Will buy again", "location": "NY"},
    ]

def _render_placeholder(title, body="This page is a placeholder. Wire it up next."):
    return render_template_string(
        """{% extends 'base.html' %}
           {% block title %}{{ title }} - Sam's Nik Naks{% endblock %}
           {% block content %}
             <section class="py-16">
               <div class="mx-auto max-w-3xl px-4">
                 <h1 class="text-3xl font-bold">{{ title }}</h1>
                 <p class="mt-4 text-slate-700">{{ body }}</p>
               </div>
             </section>
           {% endblock %}""",
        title=title,
        body=body,
        cart_count=0,
        current_year=2025,
    )

# ---------- Home (both endpoints) ----------
def _render_home():
    return render_template(
        "index.html",
        drop=_demo_drop(),
        best_sellers=_demo_products(),
        reviews=_demo_reviews(),
        cart_count=0,
        current_year=2025,
    )

@main.route("/")
def index():  # url_for('main.index')
    return render_template('index.html')

@main.route("/home")
def home():  # url_for('main.home') used by the logo link in base.html
    return _render_home()

# ---------- Shop ----------
@main.route("/shop")
@main.route("/shop/<category>")
def shop(category=None):  # url_for('main.shop', category='limited')
    products = _demo_products()
    title = "Shop" if not category else f"Shop — {category.capitalize()}"
    body = f"Showing products{(' in ' + category) if category else ''}."
    return _render_placeholder(title, body)

# Product detail
@main.route("/product/<slug>")
def product(slug):  # url_for('main.product', slug='sticker-pack')
    body = f"Product detail placeholder for “{slug}”."
    return _render_placeholder("Product", body)

# ---------- Static content pages ----------
@main.route("/about")
def about():  # url_for('main.about')
    return _render_placeholder("About")

@main.route("/faq")
def faq():  # url_for('main.faq')
    return _render_placeholder("FAQ")

@main.route("/reviews")
def reviews():  # url_for('main.reviews')
    return _render_placeholder("Reviews")

@main.route("/contact", methods=["GET", "POST"])
def contact():  # url_for('main.contact')
    if request.method == "POST":
        # Handle contact form here later
        return redirect(url_for("main.contact"))
    return _render_placeholder("Contact", "Drop us a line. (Form coming soon)")

@main.route("/privacy")
def privacy():  # url_for('main.privacy')
    return _render_placeholder("Privacy Policy")

@main.route("/returns")
def returns():  # url_for('main.returns')
    return _render_placeholder("Returns & Exchanges")

# Visit/Local pages if you add them later
@main.route("/visit")
def visit():
    return _render_placeholder("Visit Us")

# ---------- Cart / Checkout (stubs) ----------
@main.route("/cart")
def cart():  # url_for('main.cart')
    return _render_placeholder("Your Cart", "Cart UI coming soon.")

@main.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        # Kick off Stripe etc. later
        return redirect(url_for("main.index"))
    return _render_placeholder("Checkout", "Secure checkout coming soon.")

# ---------- Form endpoints used by footer/CTA ----------
@main.route("/subscribe", methods=["POST"])
def subscribe():  # form action in base footer
    email = request.form.get("email", "")
    # TODO: store email / send to ESP
    return redirect(url_for("main.index"))

@main.route("/subscribe/local", methods=["POST"])
def subscribe_local():  # form action in home callout
    zip_code = request.form.get("zip", "")
    # TODO: store zip / local list
    return redirect(url_for("main.index"))

# ---------- JS API used by Add-to-Cart button ----------
@main.route("/api/cart/add", methods=["POST"])
def api_add_to_cart():  # url_for('main.api_add_to_cart')
    # TODO: real cart logic; return updated count
    return jsonify({"count": 1})
