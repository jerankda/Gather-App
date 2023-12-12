from flask import Blueprint, render_template, request , flash 
from . import db
from .models import Gather, User, Marker
from flask_login import current_user

create = Blueprint('create', __name__)

# create a gather anf a marker and add them to databank
@create.route('/create',methods=['GET','POST'])
def create_gather():
        if request.method == 'POST':
                name = request.form.get('name')
                location = request.form.get('location')
                description = request.form.get('description')
                currentUser = current_user.id
                Host = current_user.email
                latitude = request.form.get('latitude')
                longitude = request.form.get('longitude')

                print(longitude)
                print(latitude)

                if len(name) == 0:
                        flash('Please give your Gather a name.', category='error')
                if len(location) == 0:
                        flash('Add a location to your Gather.', category='error')
                if len(description) == 0:
                        flash('Add a description.', category='error')
                else:        
                        new_gather = Gather(name=name,description = description, location = location, user_id = currentUser, Host = Host)
                        db.session.add(new_gather)
                        db.session.commit()

                        new_marker = Marker(lat=latitude, lng=longitude, gather_id=new_gather.id)
                        db.session.add(new_marker)
                        db.session.commit()

                        return render_template("gather_find.html")
                return render_template("creategather.html")                
