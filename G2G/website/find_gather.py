from flask import Blueprint, request , render_template
from .models import Gather
from . import db

find_gather = Blueprint('find_gather', __name__)


@find_gather.route("/gather_find_angezeigt", methods=['GET', 'POST'])
def start_page():

    if request.method == 'POST':
        print("TEST1")
        print("TEST1")
        print("TEST1")   
        print("TEST1")

    print("TEST2")
    print("TEST2")
    print("TEST2")   
    print("TEST2")

    Gathers = Gather.query.order_by(Gather.id).all()
    return render_template('gather_find.html', Gathers=Gathers)

