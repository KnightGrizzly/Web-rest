from flask import render_template

from app import app
from settings import config

@app.route("/")
def index():
    return render_template("index.html", name_restaurant = config.NAME_RESTAURNAT)
