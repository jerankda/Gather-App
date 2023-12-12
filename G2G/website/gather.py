from flask import Blueprint, render_template, request , flash 
from . import db
from .models import Gather, User, Marker, user_gather_association
from flask_login import current_user

gather = Blueprint('gather', __name__)

# create a gather and a marker and add them to databank
@gather.route('/create',methods=['GET','POST'])
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

#refreshing the gather-finding-page to show the gathers
@gather.route("/anzeigen", methods=['GET', 'POST'])
def start_page():

    Gathers = Gather.query.order_by(Gather.id).all()
    return render_template('gather_find.html', Gathers=Gathers)

#shows gathers which user created himself
@gather.route("/showowngather", methods=['GET', 'POST'])
def ownGather():
    user_id = current_user.id
    gathers = Gather.query.filter_by(user_id=user_id).order_by(Gather.id).all()
    return render_template('manageGather.html', Gathers=gathers)

#joining a gather
@gather.route("/join_gather", methods=['POST'])
def join_gather():

    gather_id = request.form['gather_id']
    gather = Gather.query.get(gather_id)

    user = current_user
    gather.users.append(user)

    db.session.add(gather)
    db.session.commit()

    Gathers = Gather.query.order_by(Gather.id).all()
    return render_template('gather_find.html', Gathers=Gathers)

#leaving a gather
@gather.route("/leave_gather", methods=['POST'])
def leave_gather():

    gather_id = request.form['gather_id']
    gather = Gather.query.get(gather_id)

    user = current_user

    if user in gather.users:
        gather.users.remove(user)
    
    db.session.commit()

    Gathers = Gather.query.order_by(Gather.id).all()
    return render_template('gather_find.html', Gathers=Gathers)

