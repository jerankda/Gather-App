from flask import Blueprint, request , render_template
from .models import Gather,User,user_gather_association
from . import db
from flask_login import current_user

find_gather = Blueprint('find_gather', __name__)


@find_gather.route("/angezeigen", methods=['GET', 'POST'])
def start_page():

    if request.method == 'POST':
        print("TEST1")
    print("TEST2")



    # new_gather = Gather(name='Gather Name TEST', description='Gather Description', location='Gather Location', Host='Host Name')

    # user1 = User.query.get(1)
    # user2 = User.query.get(2)
    # new_gather.users.append(user1)
    # new_gather.users.append(user2)
    # db.session.add(new_gather)
    # db.session.commit()

    # user = User.query.get(1)
    # joined_gathers = user.Gathers

    # for gather in joined_gathers:
    #    print(f"Gather Name: {gather.name}, Description: {gather.description}, Location: {gather.location}, Host: {gather.Host}")



    Gathers = Gather.query.order_by(Gather.id).all()
    return render_template('gather_find.html', Gathers=Gathers)


@find_gather.route("/join_gather", methods=['POST'])
def join_gather():

    print("TEST3")

    gather_id = request.form['gather_id']

    print(gather_id)

    gather = Gather.query.get(gather_id)

    user = current_user
    gather.users.append(user)

    db.session.add(gather)
    db.session.commit()

    joined_gathers = user.Gathers
    for gather in joined_gathers:
        print(f"Gather Name: {gather.name}, Description: {gather.description}, Location: {gather.location}, Host: {gather.Host}")


    Gathers = Gather.query.order_by(Gather.id).all()
    return render_template('gather_find.html', Gathers=Gathers)