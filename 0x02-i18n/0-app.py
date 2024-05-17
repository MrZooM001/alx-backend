#!/usr/bin/env python3
"""Module for creating basic Flask Application"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """
    Function as a route handler for the root ("/") URL.
    It returns the rendered template '0-index.html'.

    Returns:
        str: The rendered HTML content of '0-index.html' template.
    """
    return render_template("0-index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
