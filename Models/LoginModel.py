import pymongo, bcrypt
from pymongo import MongoClient


class LoginModel:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.CarbonLab
        self.Users = self.db.users

    def check_user(self, data):
        user = self.Users.find_one({"email": data.email})
        if user:
            if bcrypt.checkpw(data.pswd.encode(), user['password']):
                return user
            else:
                return False
        else:
            return False

    def updateProfile(self, data):
        update = self.Users.update_one({'email': data.email}, {'$set': data})
        return True

