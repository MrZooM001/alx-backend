#!/usr/bin/env python3
"""Module for creating basic Flask Application"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Class for app configurations"""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Function to determines the best language match for the user's browser
    settings based on the app's configured languages.

    Returns:
        str: The best matching language code, or None if no match is found.
    """
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index() -> str:
    """
    Function as a route handler for the root ("/") URL.
    It returns the rendered template '2-index.html'.

    Returns:
        str: The rendered HTML content of '0-index.html' template.
    """
    return render_template("2-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
