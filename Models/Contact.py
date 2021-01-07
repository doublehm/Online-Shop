import pymongo
from pymongo import MongoClient

class Contact:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.CarbonLab
        self.Contact = self.db.contact

    def contactRequest(self, data):
        inserted = self.Contact.insert({
                'name': data.name,
                'email': data.email,
                'content': data.content
            })

