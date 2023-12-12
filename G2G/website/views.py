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
@login_required
def map():
    return render_template("map.html",user=current_user)

# Renders the create gather page
@views.route('/creategather', methods=['GET', 'POST'])
def creategather():
    return render_template("creategather.html",user=current_user)

# Renders the gather finding page
@views.route('/gather_find', methods=['GET', 'POST'])
@login_required
def gather_find():
    return render_template("gather_find.html",user=current_user)

# Renders the contact page
@views.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")

# Renders the about us page
@views.route('/about_us', methods=['GET', 'POST'])
def about_us():
    return render_template("about_us.html")

@views.route('/manageGather', methods=['GET', 'POST'])
@login_required
def manageGather():
    return render_template("manageGather.html")

@views.route('/editGather', methods=['GET', 'POST'])
@login_required
def editGather():
    return render_template("editGather.html")

