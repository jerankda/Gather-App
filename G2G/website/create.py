from flask import Blueprint, render_template, request
from . import db
from .models import Gather

create = Blueprint('create', __name__)

@create.route('/create',methods=['GET','POST'])
def create_gather():
        if request.method == 'POST':
                name = request.form.get('name')
                location = request.form.get('location')
                description = request.form.get('description')

                new_gather = Gather(Name=name,Description = description, Location = location )
                db.session.add(new_gather)
                db.session.commit()
                print("Hundesohn")