from __future__ import annotations

from flask import flash, render_template, request

from ... import data
from . import custom


@custom.route("/how-it-works")
def how_it_works():
    return render_template("custom/how_it_works.html")


@custom.route("/start", methods=["GET", "POST"])
def intake_form():
    submitted = False
    if request.method == "POST":
        flash("Custom request received! We'll reach out with sketches soon.", "success")
        submitted = True
    return render_template("custom/intake.html", submitted=submitted)


@custom.route("/inspiration")
def inspiration():
    placeholder = "https://images.unsplash.com/photo-1512446816042-444d641267d4?auto=format&fit=crop&w=900&q=80"
    products = []
    for row in data.get_products():
        item = dict(row)
        images = [dict(img) for img in data.get_product_images(item["id"])]
        item["hero_image"] = images[0]["image_url"] if images else placeholder
        products.append(item)
    return render_template("custom/inspiration.html", products=products)
