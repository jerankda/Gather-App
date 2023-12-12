from flask import Blueprint, request , render_template
from .models import Gather,User,user_gather_association
from . import db
from flask_login import current_user

find_gather = Blueprint('find_gather', __name__)

#refreshing the gather-finding-page to show the gathers
@find_gather.route("/anzeigen", methods=['GET', 'POST'])
def start_page():

    Gathers = Gather.query.order_by(Gather.id).all()
    return render_template('gather_find.html', Gathers=Gathers)

#shows gathers which user created himself
@find_gather.route("/showowngather", methods=['GET', 'POST'])
def ownGather():
    user_id = current_user.id
    gathers = Gather.query.filter_by(user_id=user_id).order_by(Gather.id).all()
    return render_template('manageGather.html', Gathers=gathers)


#joining a gather
@find_gather.route("/join_gather", methods=['POST'])
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
@find_gather.route("/leave_gather", methods=['POST'])
def leave_gather():

    gather_id = request.form['gather_id']
    gather = Gather.query.get(gather_id)

    user = current_user

    if user in gather.users:
        gather.users.remove(user)
    
    db.session.commit()

    Gathers = Gather.query.order_by(Gather.id).all()
    return render_template('gather_find.html', Gathers=Gathers)