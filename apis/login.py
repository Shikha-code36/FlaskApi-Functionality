from flask import request, redirect, url_for, render_template, Blueprint
from projectconstant import *
import hashlib
from sendotp import *
import mongoservice

loginpage = Blueprint("loginpage", __name__)


@loginpage.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the login information from the form
        login_id = request.form['login_id']
        password = request.form['password']

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Find the user in the database
        user = mongoservice.finduser(login_id, hashed_password)
        if user:
            # Login information is correct and redirect to the homepage
            return redirect(url_for('signuppage.home'))
        else:
            # Login information is incorrect, display an error message
            return 'Invalid login'

    return render_template('login.html')
