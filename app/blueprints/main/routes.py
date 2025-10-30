from __future__ import annotations

from flask import flash, redirect, render_template, request, url_for

from ... import data
from . import main


@main.context_processor
def inject_globals():
    return {
        "cart_count": 0,
    }


@main.route("/")
@main.route("/home")
def home():
    featured_rows = [dict(row) for row in data.get_products(limited=True)]
    best_sellers_rows = [dict(row) for row in data.get_products()[:3]]
    placeholder = "https://images.unsplash.com/photo-1512446816042-444d641267d4?auto=format&fit=crop&w=900&q=80"

    for product in featured_rows + best_sellers_rows:
        images = data.get_product_images(product["id"])
        product["hero_image"] = images[0]["image_url"] if images else placeholder

    featured = featured_rows
    best_sellers = best_sellers_rows
    reviews = data.get_reviews(limit=3)
    cities = data.get_city_pages()
    return render_template(
        "home.html",
        featured=featured,
        best_sellers=best_sellers,
        reviews=reviews,
        cities=cities,
    )


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/visit")
def visit():
    cities = data.get_city_pages()
    return render_template("visit.html", cities=cities)


@main.route("/visit/<slug>")
def local_page(slug: str):
    city = data.get_city_page(slug)
    if not city:
        flash("Location not found.", "error")
        return redirect(url_for("main.visit"))
    return render_template("local.html", city=city)


@main.route("/care")
def care():
    return render_template("care.html")


@main.route("/faq")
def faq():
    return render_template("faq.html")


@main.route("/reviews")
def reviews_page():
    reviews = data.get_reviews()
    return render_template("reviews.html", reviews=reviews)


@main.route("/contact", methods=["GET", "POST"])
def contact():
    submitted = False
    if request.method == "POST":
        name = request.form.get("name", "Friend")
        flash(f"Thanks, {name}! We'll be in touch soon.", "success")
        submitted = True
    return render_template("contact.html", submitted=submitted)


@main.route("/policies/shipping")
def shipping_policy():
    return render_template("policies/shipping.html")


@main.route("/policies/returns")
def returns_policy():
    return render_template("policies/returns.html")


@main.route("/policies/privacy")
def privacy_policy():
    return render_template("policies/privacy.html")


@main.route("/policies/terms")
def terms_policy():
    return render_template("policies/terms.html")


@main.route("/subscribe", methods=["POST"])
def subscribe():
    flash("Thanks for subscribing!", "success")
    return redirect(url_for("main.home"))


@main.route("/subscribe/local", methods=["POST"])
def subscribe_local():
    zip_code = request.form.get("zip", "")
    if not zip_code:
        flash("Please include a ZIP code.", "error")
    else:
        flash("We'll let you know about local pop-ups!", "success")
    return redirect(url_for("main.home"))
