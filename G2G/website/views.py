from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

# Renders home template
@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

# Renders explore template
@views.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    return render_template("explore.html",user=current_user)

# Renders map template
@views.route('/map', methods=['GET', 'POST'])
def map():
    return render_template("map.html",user=current_user)

@views.route('/creategather', methods=['GET', 'POST'])
def creategather():
    return render_template("creategather.html",user=current_user)
