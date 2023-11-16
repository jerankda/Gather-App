from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
#@login_required
def home():

    return render_template("home.html", user=current_user)

@views.route('/user', methods=['GET', 'POST'])
@login_required
def logged():

    return render_template("logedin.html", user=current_user)

@views.route('/explore',methods = ['GET','POST'])
def explore():
    return render_template("explore.html")

@views.route('/map',methods = ['GET','POST'])
def map():
    return render_template("map.html")