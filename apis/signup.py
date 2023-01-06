from flask import request, redirect, url_for, render_template, Blueprint
import pyotp
import hashlib
from projectconstant import *
from sendotp import *
import mongoservice

signuppage = Blueprint("signuppage", __name__)


# Generate a secret key for OTPs
secret_key = pyotp.random_base32()

@signuppage.route('/')
def home():
    return render_template('home.html')


@signuppage.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        email_exists= mongoservice.checkuseremail(email)
        if email_exists:
            return render_template('email-exists.html', email=email)

        phone_exists=mongoservice.checkuserphone(phone)
        if phone_exists:
            return render_template('phone-exists.html', phone=phone)
        
        else:
            # Generate OTPs for email and phone
            otp = pyotp.TOTP(secret_key).now()
            #phone_otp = pyotp.TOTP(secret_key).now()

            # Send the OTPs to the user
            send_email(email, otp)
            send_sms(phone, otp)

            # Store the user's information in the database
            user = {
                'name': name,
                'phone': phone,
                'email': email,
                'password': hashed_password,
                'otp': otp
            }
            mongoservice.createuser(user)

            # Redirect to the OTP confirm page
            return redirect(url_for('confirmotp.confirm_otp'))
    return render_template('signup.html')

