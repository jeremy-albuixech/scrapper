#!/usr/bin/env python3
import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask import render_template
from logzero import logger
from dotenv import load_dotenv

def create_app(config=None):
    app = Flask(__name__)

    load_dotenv()
    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})
    CORS(app)

    from scrapper import google_config
    from scrapper import reddit

    app.register_blueprint(google_config.bp)
    app.register_blueprint(reddit.bp)

    app.add_url_rule("/", endpoint="index")
    
    return app