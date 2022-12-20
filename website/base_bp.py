from flask import Blueprint, render_template, redirect, url_for

views = Blueprint(__name__, "views")


@views.route("/")
def home():
    return render_template("index.html", var="Some var")


@views.route("/<var>")
def home_but_cooler(var):
    return render_template("index.html", var=var)

@views.route("/home")
def back_home():
    return redirect(url_for("base_bp.home"))