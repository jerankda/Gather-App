from flask import Blueprint, render_template, request , flash , jsonify , redirect, url_for
from . import db
from .models import Gather, User, Marker, user_gather_association
from flask_login import current_user, login_required

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

# Giving the map the location and name of all already set pins
@gather.route('/get_markers')
def get_markers():
    markers = Marker.query.all()
    markers_data = [{'lat': marker.lat, 'lng': marker.lng, 'name': marker.gather.name} for marker in markers]
    return jsonify(markers_data)
    
@gather.route('/editGather', methods=['GET', 'POST'])
@login_required
def editGather():
    gather_id = request.form['gather_id']
    gather = Gather.query.get(gather_id)
    return render_template("editGather.html",Gather=gather)
    
@gather.route('/saveChanges',methods=['GET','POST'])
@login_required
def saveChanges():
      if request.method == 'POST':
        new_Name = request.form.get('name')
        new_location = request.form.get('location')
        new_description = request.form.get('description')
        gather_id = request.form['gather_id']

        gather = Gather.query.get(gather_id)
        

        # Update the new Entries
        gather.name = new_Name
        gather.location = new_location
        gather.description = new_description

        db.session.commit()
        return render_template("manageGather.html",Gather=gather)

@gather.route('/deleteGather',methods=['GET','POST'])
@login_required
def deleteGather():
      if request.method == 'POST':
        gatherId = request.form['gather_id']
        db.session.query(user_gather_association).filter_by(gather_id=gatherId).delete(all)
        db.session.query(Marker).filter_by(gather_id=gatherId).delete()
        db.session.query(Gather).filter_by(id=gatherId).delete()
        db.session.commit()
        return render_template("manageGather.html")

@gather.route('/extendedGather',methods=['GET','POST'])
@login_required
def extendedGather():
    gather_id = request.form['gather_id']
    gather = Gather.query.get(gather_id)
    return render_template("extendedGather.html", Gather = gather)