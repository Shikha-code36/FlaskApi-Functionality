import smtplib
import requests
from projectconstant import *

def send_email(to, otp):
    # Set up the SMTP server
    server = smtplib.SMTP(SOURCE)
    server.starttls()
    server.login(EMAIL, APIKEY_EMAIL)

    # Send the email
    from_add = EMAIL
    subject = 'OTP for registration'
    body = 'Your OTP is: {}'.format(otp)    
    msg = 'Subject: {}\n\n{}'.format(subject, body)
    sent_email= server.sendmail(from_add, to, msg)
    if not sent_email:
        print('Message successfully delivered')
    else:
        print('Failed to deliver message to: {}'.format(sent_email))

    # Close the SMTP server
    server.quit()


def send_sms(to, otp):
    # Set up the request parameters
    url = SMS_URL
    payload = {
        'To': to,
        'From': PHONENO,
        'Body': 'Your OTP is: {}'.format(otp)
    }
    auth = (SMS_API_SSID, SMS_API_KEY)

    # Send the request
    response = requests.post(url, data=payload, auth=auth)

    # Check the response status code
    if response.status_code != 201:
        raise Exception('Failed to send SMS: {}'.format(response.text))
