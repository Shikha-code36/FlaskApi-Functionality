from flask import request, redirect, url_for, render_template, Blueprint
import pyotp
from projectconstant import *
from sendotp import *
import mongoservice

forgotpass = Blueprint("forgotpass", __name__)


# Generate a secret key for OTPs
secret_key = pyotp.random_base32()

@forgotpass.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Get the login ID from the form
        login_id = request.form['login_id']

        # Find the user in the database
        user = mongoservice.forgotpassword(login_id)
        if user:
            # Generate an OTP
            otp = pyotp.TOTP(secret_key).now()

            # Send the OTP to the user
            if 'email' in user:
                send_email(user['email'], otp)
            else:
                send_sms(user['phone'], otp)

            # Update the user's OTP in the database
            mongoservice.updateOTP(user, otp)

            # Redirect to the OTP confirm page
            return redirect(url_for('confirmotp.confirm_otp'))
        else:
            # Login ID is not registered, display an error message
            return 'Login ID is not registered'

    return render_template('forgot_password.html')

