import bcrypt, pymongo
from pymongo import MongoClient


class Posts:
    def __init__(self):
        slef.client = MongoClient()
        slef.db = self.client.CarbonLab
        self.Posts = self.db.posts

    

