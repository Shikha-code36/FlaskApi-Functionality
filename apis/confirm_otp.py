from flask import request, redirect, url_for, render_template, Blueprint
from projectconstant import *
from sendotp import *
import mongoservice

confirmotp = Blueprint("confirmotp", __name__)

@confirmotp.route('/confirm_otp', methods=['GET', 'POST'])
def confirm_otp():
    if request.method == 'POST':
        # Get the OTPs from the form
        enter_otp = request.form['enter_otp']
        confirm_otp = request.form['confirm_otp']

        # Find the user in the database
        user = mongoservice.finduserwithOTP(enter_otp)
        if user:
            # OTPs are valid, log the user in and redirect to the homepage
            return redirect(url_for('signuppage.home'))
        else:
            # OTPs are invalid, display an error message
            return 'Invalid OTPs'

    return render_template('confirm_otp.html')



