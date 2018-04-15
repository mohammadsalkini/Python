import cs50
import re
from flask import Flask, abort, redirect, render_template, request
from html import escape
from werkzeug.exceptions import default_exceptions, HTTPException
from vigenere import Vigenere

# Web app
app = Flask(__name__)


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Handle requests for / via GET (and POST)"""
    return render_template("index.html")


@app.route("/convert", methods=["POST","GET"])
def convert():
    """Handle requests for /compare via POST"""
    if request.method == "GET":
        return render_template("index.html")

    key = request.form.get("key")

    if not request.files["file"]:
        abort(400, "Missing file")

    if not request.form.get("key"):
        abort(400, "Missing key")

    if not key.isalpha():
        abort(400, "Invalid key")

    try:
        file = request.files["file"].read().decode("utf-8")
    except Exception:
        abort(400, "invalid file")


    if not request.form.get("algorithm"):
        abort(400, "missing algorithm type")
    elif request.form.get("algorithm") == "encrypt":
        conversion = Vigenere().cipher_vigenere(file, key)
    elif request.form.get("algorithm") == "decrypt":
        conversion = Vigenere().decrypt_vigenere(file, key)
    # Read files

    return render_template("convert.html", convert = conversion )


@app.errorhandler(HTTPException)
def errorhandler(error):
    """Handle errors"""
    return render_template("error.html", error=error), error.code


# https://github.com/pallets/flask/pull/2314
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
