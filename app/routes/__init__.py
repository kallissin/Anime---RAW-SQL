from flask import Blueprint, Flask
from .animes_blueprint import bp_animes

def init_app(app: Flask):
    app.register_blueprint(bp_animes)
