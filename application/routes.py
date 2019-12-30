import random, uuid
from application import simpleApp, db
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from .models import AsylumSeeker, Users

# routing
@simpleApp.route('/')
@simpleApp.route('/index')
def index():
    return render_template('index.html')

# save email to database and send to success page
@simpleApp.route('/post', methods=['POST'])
def post():
    email, first_name, last_name = None, None, None
    if request.method == 'POST':
        user_id = random.randrange(5000)
        asylum_seeker_id = uuid.uuid4()
        email = request.form['email']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        preferred_language = request.form['language']
        # create a local instance of the Users class
        users_data = Users(user_id, email, preferred_language)
        # create a local instance of the AsylumSeeker class
        seeker_data = AsylumSeeker(asylum_seeker_id, user_id, first_name, last_name)
        # stage the new instances to be added to the database
        db.session.add(users_data)
        db.session.add(seeker_data)
        # commit the change
        db.session.commit()
    return render_template('success.html', firstname=first_name, lastname=last_name)
