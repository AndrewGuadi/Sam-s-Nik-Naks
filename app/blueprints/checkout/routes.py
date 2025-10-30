from __future__ import annotations

from flask import flash, redirect, render_template, request, url_for

from . import checkout


@checkout.route("/cart")
def cart():
    return render_template("checkout/cart.html")


@checkout.route("/checkout", methods=["GET", "POST"])
def checkout_view():
    if request.method == "POST":
        flash("Stripe checkout session will start soon.", "success")
        return redirect(url_for("checkout.success"))
    return render_template("checkout/checkout.html")


@checkout.route("/checkout/success")
def success():
    return render_template("checkout/success.html")
