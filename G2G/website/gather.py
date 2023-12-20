from flask import Blueprint, render_template, request , flash , jsonify
from . import db
from .models import Gather, User, Marker, user_gather_association, Message
from flask_login import current_user, login_required
from datetime import datetime

gather = Blueprint('gather', __name__)

# create a gather and a marker and add them to databank
@gather.route('/create',methods=['GET','POST'])
@login_required
def create_gather():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        description = request.form.get('description')
        currentUser = current_user.id
        Host = current_user.email
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        if latitude == '':
            latitude = 1.111111111111 
            longitude = 1.111111111111

        if date_str:
            year = int(date_str.split('-')[0])
            if year < 1900:
                flash('Year must be after 1900. Please select a valid date.', category='error')
                return render_template("creategather.html")

        if len(name) == 0:
            flash('Please give your Gather a name.', category='error')
        elif len(location) == 0:
            flash('Add a location to your Gather.', category='error')
        elif len(description) == 0:
            flash('Add a description.', category='error')
        else:
            # Convert the date and time strings to date and time objects
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
            time_obj = datetime.strptime(time_str, '%H:%M').time() if time_str else None

            new_gather = Gather(name=name, description=description, location=location, 
                                Date=date_obj, Time=time_obj, user_id=currentUser, Host=Host)
            db.session.add(new_gather)
            db.session.commit()

            new_marker = Marker(lat=latitude, lng=longitude, gather_id=new_gather.id)
            db.session.add(new_marker)
            db.session.commit()

            return render_template("gather_find.html")
        return render_template("creategather.html")                

#refreshing the gather-finding-page to show the gathers
@gather.route("/anzeigen", methods=['GET', 'POST'])
@login_required
def start_page():

    Gathers = Gather.query.order_by(Gather.id).all()
    return render_template('gather_find.html', Gathers=Gathers)

#shows gathers which user created himself
@gather.route("/showowngather", methods=['GET', 'POST'])
@login_required
def ownGather():
    user_id = current_user.id
    gathers = Gather.query.filter_by(user_id=user_id).order_by(Gather.id).all()
    return render_template('manageGather.html', Gathers=gathers)

#joining a gather
@gather.route("/join_gather", methods=['POST'])
@login_required
def join_gather():

    gather_id = request.form['gather_id']
    gather = Gather.query.get(gather_id)

    user = current_user

    if user not in gather.users:
        gather.users.append(user)
        db.session.add(gather)
        db.session.commit()

    marker = Marker.query.filter_by(gather_id=gather_id).first()

    markerLat = marker.lat
    markerLng = marker.lng

    messages = Message.query.order_by(Message.created_at).all()

    return render_template("extendedGather.html", Gather = gather, markerLat=markerLat, markerLng=markerLng, messages=messages)

#leaving a gather
@gather.route("/leave_gather", methods=['POST'])
@login_required
def leave_gather():

    gather_id = request.form['gather_id']
    gather = Gather.query.get(gather_id)

    user = current_user

    if user in gather.users:
        gather.users.remove(user)
    
    db.session.commit()
    marker = Marker.query.filter_by(gather_id=gather_id).first()

    markerLat = marker.lat
    markerLng = marker.lng

    messages = Message.query.order_by(Message.created_at).all()

    return render_template("extendedGather.html", Gather = gather, markerLat=markerLat, markerLng=markerLng, messages=messages)

#kick User from Gather
@gather.route("/kickUser", methods=['POST'])
@login_required
def kickUser():

    gather_id = request.form['gather_id']
    gather = Gather.query.get(gather_id)

    user_id = request.form['user_id']
    user = User.query.get(user_id)

    if user in gather.users:
        gather.users.remove(user)
    
    db.session.commit()
    return render_template('editGather.html',Gather=gather)

# returning the location and names of all already set pins
@gather.route('/get_markers')
@login_required
def get_markers():
    markers = Marker.query.all()
    markers_data = [{'lat': marker.lat, 'lng': marker.lng, 'name': marker.gather.name, 'id': marker.gather.id } for marker in markers]
    return jsonify(markers_data)


# loading the map, but with the view on the last gather
@gather.route('/loadMapWithCoordinates', methods=['POST'])
@login_required
def loadMapWithCoordinates():

    gather_id = request.form['gather_id']
    marker = Marker.query.filter_by(gather_id=gather_id).first()
    markerLat = marker.lat
    markerLng = marker.lng
    return render_template("map.html", markerLat=markerLat,markerLng=markerLng, gather_id=gather_id)


#Get the Gather ID and load the editGather page
@gather.route('/editGather', methods=['GET', 'POST'])
@login_required
def editGather():
    gather_id = request.form['gather_id']
    gather = Gather.query.get(gather_id)
    return render_template("editGather.html",Gather=gather)
    
#Get the changes to the Gather and commit them to the Database
@gather.route('/saveChanges',methods=['GET','POST'])
@login_required
def saveChanges():
    if request.method == 'POST':
        new_Name = request.form.get('name')
        new_location = request.form.get('location')
        new_description = request.form.get('description')
        new_Time_str = request.form.get('time')
        new_Date_str = request.form.get('date')
        gather_id = request.form['gather_id']

        if new_Date_str:
            year = int(new_Date_str.split('-')[0])
            if 3000  < year < 1900:
                flash('Year must be between 1900 and 3000. Please select a valid date.', category='error')
                return render_template("manageGather.html")

        gather = Gather.query.get(gather_id)

        # Convert the date and time strings to date and time objects
        if new_Date_str:
            new_Date = datetime.strptime(new_Date_str, '%Y-%m-%d').date()
            gather.Date = new_Date

        if new_Time_str:
            try:
                new_Time = datetime.strptime(new_Time_str, '%H:%M').time()
            except ValueError:
                try:
                    new_Time = datetime.strptime(new_Time_str, '%H:%M:%S').time()
                except ValueError:
                    flash('Invalid time format. Please use HH:MM or HH:MM:SS.', category='error')
                    return render_template("manageGather.html", Gather=gather)
            gather.Time = new_Time

        # Update the new Entries
        gather.name = new_Name
        gather.location = new_location
        gather.description = new_description

        db.session.commit()
        return render_template("manageGather.html", Gather=gather)
    
#Delete a Gather and all data connected to it
@gather.route('/deleteGather',methods=['GET','POST'])
@login_required
def deleteGather():
      if request.method == 'POST':
        gatherId = request.form['gather_id']
        db.session.query(user_gather_association).filter_by(gather_id=gatherId).delete(all)
        db.session.query(Message).filter_by(gather_id=gatherId).delete()
        db.session.query(Marker).filter_by(gather_id=gatherId).delete()
        db.session.query(Gather).filter_by(id=gatherId).delete()
        db.session.commit()
        return render_template("manageGather.html")

#Get the Gather, the coordinates of its Marker and its messages und give them to the extendedGather.html
@gather.route('/extendedGather',methods=['GET','POST'])
@login_required
def extendedGather():
    gather_id = request.form['gather_id']
    gather = Gather.query.get(gather_id)
    marker = Marker.query.filter_by(gather_id=gather_id).first()
    print(gather_id)
    markerLat = marker.lat
    markerLng = marker.lng

    messages = Message.query.order_by(Message.created_at).all()

    return render_template("extendedGather.html", Gather = gather, markerLat=markerLat, markerLng=markerLng, messages=messages)

#Get the Gather, the coordinates of its Marker and its messages und give them to the extendedGather.html, executed by JavaScript
@gather.route('/render-extended-gather', methods=['GET'])
@login_required
def render_extended_gather():
    gather_id = request.args.get('gather_id')
    markerLat = request.args.get('markerLat')
    markerLng = request.args.get('markerLng')

    gather = Gather.query.get(gather_id)
    messages = Message.query.order_by(Message.created_at).all()

    return render_template("extendedGather.html", Gather=gather, markerLat=markerLat, markerLng=markerLng, messages=messages)

#Get the message and commit it to the database
@gather.route('/sendMessage', methods=['POST'])
@login_required
def sendMessage():

    text = request.form['content']
    gather_id = request.form['gather_id']
    user = current_user.email

    if text != '':
        new_message = Message(user=user,content=text, gather_id=gather_id)
        db.session.add(new_message)
        db.session.commit()


    gather = Gather.query.get(gather_id)
    marker = Marker.query.filter_by(gather_id=gather_id).first()
    markerLat = marker.lat
    markerLng = marker.lng
    messages = Message.query.order_by(Message.created_at).all()

    return render_template("extendedGather.html", Gather = gather, markerLat=markerLat, markerLng=markerLng, messages=messages)
