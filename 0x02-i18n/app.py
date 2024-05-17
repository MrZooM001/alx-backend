#!/usr/bin/env python3
"""Module for creating basic Flask Application"""
import datetime
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime
from typing import Dict, Union
from pytz import timezone, exceptions as tz_ex


class Config:
    """Class for app configurations"""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False

babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id) -> Union[Dict, None]:
    """Retrieves user based on the user ID in the URL."""
    return users.get(int(user_id), 0)


@app.before_request
def before_request() -> str:
    """
    Function uses a Flask before_request handler to run before each request
    and sets the user in the Flask global context (g) based on the user ID
    from the URL query parameters.
    """
    logged_user = request.args.get("login_as", 0)
    setattr(g, "user", get_user(logged_user))


@babel.timezoneselector
def get_timezone() -> str:
    """
    Function that determines the user's timezone based.
    first checks if a timezone is provided in the URL query parameters.
    then, checks if the user's timezone is set in the user data.
    otherwise, it uses the default timezone from the app's configuration.
    If the provided timezone is not valid, it returns the default timezone.
    """
    timezone_from_url = request.args.get("timezone")
    try:
        timezone(timezone_from_url).zone
        if timezone_from_url:
            return timezone_from_url

        if g.user and g.user["timezone"]:
            return g.user["timezone"]

    except tz_ex.UnknownTimeZoneError:
        return app.config["BABEL_DEFAULT_TIMEZONE"]


@babel.localeselector
def get_locale() -> str:
    """
    Function to determines the best language match for the user's browser
    settings based on the app's configured languages.

    Returns:
        str: The best matching language code, or None if no match is found.
    """
    locale_from_url = request.args.get("locale")
    if locale_from_url and locale_from_url in app.config["LANGUAGES"]:
        return locale_from_url

    if g.user and g.user["locale"] in app.config["LANGUAGES"]:
        return g.user["locale"]

    locale_from_header = request.headers.get("locale")
    if locale_from_header and locale_from_header in app.config["LANGUAGES"]:
        return locale_from_header

    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index() -> str:
    """
    Function as a route handler for the root ("/") URL.
    It returns the rendered template 'index.html'.

    Returns:
        str: The rendered HTML content of 'index.html' template.
    """
    g.time = format_datetime()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
