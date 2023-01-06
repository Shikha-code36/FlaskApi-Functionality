from pymongo import MongoClient
from projectconstant import *


# Connect to the MongoDB database
mongo_client = MongoClient(MONGO_STRING)
db = mongo_client['authentication']

def createuser(user):
    return db.users.insert_one(user)

def checkuseremail(email):
    return db.users.find_one({'$or': [{'email': email}]})
    
def checkuserphone(phone):
    user = db.users.find_one({'$or': [{'phone': phone}]})
    if user:
        return "Exists"

def finduserwithOTP(otp):
    user=db.users.find_one({'otp': otp})
    return user

def finduser(login_id,hashed_password):
    user = db.users.find_one({'$or': [{'email': login_id}, {'phone': login_id}], 'password': hashed_password})
    return user

def userprofile(userid):
    user = db.users.find_one({'_id': userid})
    return user

def forgotpassword(login_id):
    user = db.users.find_one({'$or': [{'email': login_id}, {'phone': login_id}]})
    return user

def updateOTP(user,otp):
     return db.users.update_one({'_id': user['_id']}, {'$set': {'otp': otp}})

def storelist(data):
    return db.lists.insert_one({'data': data})

def findlist():
    return db.lists.find()

def findlistbyid(list_id):
    return db.lists.find_one({'_id': list_id})