from __future__ import annotations

import json

from flask import abort, render_template, request

from ... import data
from . import shop


PLACEHOLDER_IMAGE = "https://images.unsplash.com/photo-1512446816042-444d641267d4?auto=format&fit=crop&w=900&q=80"


def _enrich(products):
    enriched = []
    for row in products:
        item = dict(row)
        images = [dict(img) for img in data.get_product_images(item["id"])]
        item["images"] = images
        item["hero_image"] = images[0]["image_url"] if images else PLACEHOLDER_IMAGE
        enriched.append(item)
    return enriched


@shop.app_context_processor
def inject_filters():
    return {
        "categories": [dict(row) for row in data.get_categories()],
    }


@shop.route("/")
def list_products():
    products = _enrich(data.get_products())
    return render_template("shop/list.html", products=products, title="All Products")


@shop.route("/limited")
def limited():
    products = _enrich(data.get_products(limited=True))
    return render_template("shop/list.html", products=products, title="Limited Drops")


@shop.route("/seasonal")
def seasonal():
    products = _enrich([p for p in data.get_products() if p["seasonal"]])
    return render_template("shop/list.html", products=products, title="Seasonal Highlights")


@shop.route("/category/<slug>")
def category(slug: str):
    category_row = data.get_category_by_slug(slug)
    if not category_row:
        abort(404)
    products = _enrich(data.get_products(category_slug=slug))
    return render_template("shop/category.html", category=dict(category_row), products=products)


@shop.route("/product/<slug>")
def product(slug: str):
    product_row = data.get_product_by_slug(slug)
    if not product_row:
        abort(404)
    product_dict = dict(product_row)
    images = [dict(img) for img in data.get_product_images(product_row["id"])]
    personalization = json.loads(product_row["personalization_schema"]) if product_row["personalization_schema"] else {}
    options = json.loads(product_row["options"]) if product_row["options"] else {}
    related = _enrich([p for p in data.get_products(category_slug=product_row["category_slug"]) if p["slug"] != slug][:3])
    return render_template(
        "shop/product.html",
        product=product_dict,
        images=images,
        personalization=personalization,
        options=options,
        related=related,
    )


@shop.route("/search")
def search():
    term = request.args.get("q", "").strip()
    products = _enrich(data.get_products(search_term=term)) if term else []
    return render_template("shop/search.html", term=term, products=products)
