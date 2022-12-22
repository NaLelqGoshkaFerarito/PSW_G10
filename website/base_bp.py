from flask import Blueprint, render_template, redirect, url_for
import requests
import json

views = Blueprint(__name__, "views")


@views.route("/")
def home():
    jsonb = json.dumps(requests.get("http://127.0.0.1:7777/devices/all/").json())
    lst_x = list()
    lst_y = list()
    for packet in jsonb:
        return render_template("index.html", sth=jsonb)


# @views.route("/<var>")
# def home_but_cooler(var):
#     return render_template("index.html", var=var)

# @views.route("/home")
# def back_home():
#     return redirect(url_for("base_bp.home"))