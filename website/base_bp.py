from flask import Blueprint, render_template, redirect, url_for
import requests
import json

views = Blueprint(__name__, "views")


@views.route("/")
def home():
    jsonb = requests.get("http://127.0.0.1:7777/statuses/?number=10").json().replace("'", '"')
    lst_x = list()
    lst_y = list()
    # for packet in jsonb:
    #     lst_x.append(packet["time"])
    #     lst_y.append(packet["light"])
    return render_template("index.html", sth=jsonb)


# @views.route("/<var>")
# def home_but_cooler(var):
#     return render_template("index.html", var=var)

# @views.route("/home")
# def back_home():
#     return redirect(url_for("base_bp.home"))