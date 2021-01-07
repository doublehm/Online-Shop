import pymongo
from pymongo import MongoClient
import bcrypt

class RegisterModel:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.CarbonLab
        self.Users = self.db.users


    def insert_users(self, data):
        hashed = bcrypt.hashpw(data.pswd.encode(), bcrypt.gensalt())
        id = self.Users.insert({"name": data.name, "telno": data.telno, "email": data.email, "password": hashed,
                                "address": '', "city": '', "state": '', "zipcode": '', "order_value": ''})
        print("uid", id)

    def check_if_user_exists(self, data):
        user_existance = self.Users.find_one({"email": data.email})
        if user_existance:
            return True
        else:
            return False
