import datetime
import humanize
import bcrypt, pymongo
from pymongo import MongoClient
from bson import ObjectId


class Posts:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.CarbonLab
        self.Posts = self.db.posts
        self.Users = self.db.users
        self.Comments = self.db.comments
    
    def insert_posts(self, data):
        inserted = self.Posts.insert({'dateAdded': datetime.datetime.now(),
                                      'post_number': data.number,
                                      'image': data.imageUrl,
                                      'title':data.title,
                                      'article': data.article})

    def get_posts(self):
        all_posts = self.Posts.find().sort("dateAdded", -1)
        new_posts = []

        for post in all_posts:
            post['timeStamp'] = humanize.naturaltime(datetime.datetime.now() - post['dateAdded'])
            post['old_comments'] = self.Comments.find({"post_id": str(post['_id'])})
            post['comments'] = []

            for comment in post['old_comments']:
                print(comment)
                post['comments'].append(comment)

            new_posts.append(post)

        return new_posts

    def get_latest_posts(self):
        all_posts = self.Posts.find().sort("dateAdded", -1)
        new_posts = []

        n = 0
        for post in all_posts:
            while n<3:
                new_posts.append(post)
                n+=1
                break

        return new_posts
    
    def add_comment(self, data):
        inserted = self.Comments.insert({'post_id': data['post_id'], 'comment-text': data['commenttext'],
            'dateAdded': datetime.datetime.now(), 'username': data['username']})

        return inserted

    def find_post(self, id):
        post = self.Posts.find_one({"post_number": str(id)})
        post['timeStamp'] = humanize.naturaltime(datetime.datetime.now() - post['dateAdded'])
        post['old_comments'] = self.Comments.find({"post_id": str(post['_id'])})
        post['comments'] = []

        for comment in post['old_comments']:
            print(comment)
            post['comments'].append(comment)
        return post

    def del_post(self, id):
        delete_post = self.Posts.delete_one({"post_number": str(id)})

