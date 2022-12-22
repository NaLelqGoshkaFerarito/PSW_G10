from flask import Blueprint, render_template, redirect, url_for
import requests
import json

views = Blueprint(__name__, "views")


@views.route("/")
def home():
    jsonb = json.loads(json.dumps(requests.get("http://127.0.0.1:7777/statuses/?number=4").json()))
    data = list()
    for packet in jsonb:
        data.append((packet["temperature"],  packet["pressure"]))
    return render_template("index.html", data_js=data)


# @views.route("/<var>")
# def home_but_cooler(var):
#     return render_template("index.html", var=var)

# @views.route("/home")
# def back_home():
#     return redirect(url_for("base_bp.home"))