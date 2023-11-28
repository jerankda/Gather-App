from flask import Blueprint, render_template, request , flash
from . import db
from .models import Gather

create = Blueprint('create', __name__)

@create.route('/create',methods=['GET','POST'])
def create_gather():
        if request.method == 'POST':
                name = request.form.get('name')
                location = request.form.get('location')
                description = request.form.get('description')

                if len(name) == 0:
                        flash('Please give your Gather a name.', category='error')
                if len(location) == 0:
                        flash('Add a location to your Gather.', category='error')
                if len(description) == 0:
                        flash('Add a description.', category='error')
                else:        
                        new_gather = Gather(name=name,description = description, location = location )
                        db.session.add(new_gather)
                        db.session.commit()
                        return render_template("explore.html")    # !!FÜR findGather.html AUSTAUSCHEN !!
                return render_template("creategather.html")                
