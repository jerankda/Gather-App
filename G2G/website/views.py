from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

# Renders home template
@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

# Renders explore template, to see all of Gathers functions
@views.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    return render_template("explore.html",user=current_user)

# Renders map template, to show all the Gathers locations
@views.route('/map', methods=['GET', 'POST'])
@login_required
def map():
    return render_template("map.html",user=current_user)

# Renders the create Gather page, to create your won Gather
@views.route('/creategather', methods=['GET', 'POST'])
@login_required
def creategather():
    return render_template("creategather.html",user=current_user)

# Renders the Gather finding page, that shows you all the existing Gathers
@views.route('/gather_find', methods=['GET', 'POST'])
@login_required
def gather_find():
    return render_template("gather_find.html",user=current_user)

# Renders the contact page, with our contact information
@views.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")

# Renders the about us page, with our introduction 
@views.route('/about_us', methods=['GET', 'POST'])
def about_us():
    return render_template("about_us.html")

# Render the manage Gather page, which shosw your own Gathers
@views.route('/manageGather', methods=['GET', 'POST'])
@login_required
def manageGather():
    return render_template("manageGather.html")



