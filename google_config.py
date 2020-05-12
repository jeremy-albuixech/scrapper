from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from gmusicapi import Mobileclient

import re

g_music = Mobileclient()

bp = Blueprint("google_config", __name__)


@bp.route("/google_config", methods=("GET", "POST"))
def google_config():

    """Fetch google token and save form data."""
    if request.method == "POST":  
        android_id = request.form["androidid"]
        error = None         

        if not android_id:
            error = "Android ID is required."

        if error is not None:
            flash(error)
        else:
            try:
                if g_music.is_authenticated() is False:
                    g_music.oauth_login(android_id)
            except Exception as googleError: 
                return render_template("google/index.html", error=googleError)
    return render_template("google/index.html", google_auth = g_music.is_authenticated())

@bp.route("/google_logout", methods=["POST"])
def google_logout():   
    try:
        g_music.logout()
        return redirect(url_for('google_config.google_config'))
    except Exception as googleError: 
        print(googleError)

    return render_template("google/index.html")