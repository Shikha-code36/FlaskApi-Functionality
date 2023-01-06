from flask import Flask
from projectconstant import *

from apis.signup import signuppage
from apis.confirm_otp import confirmotp
from apis.login import loginpage
from apis.forgot_password import forgotpass
from apis.json_validate import jsonValidate

# Create the Flask app
app = Flask(__name__, template_folder='template')
app.secret_key = APPSECRET

app.register_blueprint(signuppage)
app.register_blueprint(confirmotp)
app.register_blueprint(loginpage)
app.register_blueprint(forgotpass)
app.register_blueprint(jsonValidate)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
