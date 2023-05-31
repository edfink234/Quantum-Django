import json
import sys
from time import sleep
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from random import randint
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import asyncio
from channels.exceptions import ChannelFull
from pymongo import MongoClient
import re

class ZMQChannels(AsyncWebsocketConsumer):
    consumers = 0 #this is a class variable, referred to as ZMQChannels.consumers
    users = set() #set of unique users, not used, but hey, if you need it, why not
    async def connect(self):
        print("self.channel_name in ZMQChannels =",self.channel_name)
        self.room_name = self.scope["url_route"]["kwargs"]
        print(self.room_name) #Empty dictionary
        self.room_group_name = "ZMQ" #Setting the group name to ZMQ
        print(self.room_group_name) #ZMQ
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        
        self.groups.append(self.room_group_name)
        self.consumer = ZMQChannels.consumers #the `n'th` consumer, not used though...
        await self.accept() #accept the connection
        ZMQChannels.consumers += 1
    async def disconnect(self, close_code):
        # Leave room group
        print('disconnecting')
        ZMQChannels.consumers-=1
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
    
    #Receives data from myfirst.html and sends it to server.py, called by chatsocket.send
    async def receive(self, text_data):
        try:
            client = MongoClient()
            db = client.test_database #stores the database for all of the users
            
            #get mongodb data if it's an html string
            regex = r"user = (.+);" #this part matches the string "user = " followed by 1 or more instances of anything (.+) followed by a semicolon ;
            html_string = text_data #copy text_data to html_string since we want to modify it potentially
            
            match = re.search(regex, html_string) #search through html_string for regex pattern
            if match: #if regex pattern found
                user = match.group(1) #get part matched by (.+), the user's username
                print(user)
                ZMQChannels.users.add(user) #add user to set of users for the heck of it.
                
                #extract the html part of the string, i.e., the data
                html_string = html_string[match.end()+1:].replace("\\", "")
                
                #Now, add/update the user with the corresponding html string
                if db.posts.find_one({"user": user}):
                    db.posts.find_one_and_update({"user": user}, { '$set': {"user": user, "index_data":html_string}})
                else: #if user is not registered in the mongdb database
                    #add the user with the user's data
                    db.posts.insert_one({"user": user, "index_data":html_string})
                
                return #if there was a match, then we're done here: we just needed to store some data in mongodb for this case
            elif text_data.count(",") == 15: #then text_data corresponds to the voltage data, i.e., the 16 line graphs
                activatedChannels = text_data.split(",") #now it's a list of 'true' or 'false' strings
                print("activatedChannels =",activatedChannels)
                activatedChannels = [False if i == 'false' else True for i in activatedChannels] #now it's a list of booleans
                #Now, add/update the user with the corresponding html string
                                
                user = str(self.scope["user"]) #self.scope["user"] is of type <class 'channels.auth.UserLazyObject'>
                
                
                if db.posts.find_one({"user": user}):
                    db.posts.find_one_and_update({"user": user}, { '$set': {"user": user, "activatedChannels":activatedChannels}})
                else: #if user is not registered in the mongdb database
                    #add the user with the user's data
                    db.posts.insert_one({"user": user, "activatedChannels": activatedChannels})
                return
            
            await self.channel_layer.send("ZMQ", {"type": "chat.message", "text_data": json.dumps(text_data)}) #send data to server.py
        except ChannelFull:
            pass

    #Sends data from server.py to Raman.html
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"event": event}))


#https://pymongo.readthedocs.io/en/stable/tutorial.html
#from pymongo import MongoClient
#client = MongoClient()
#db = client.test_database
#db.posts
#import datetime
#post = {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"], "date": datetime.datetime.utcnow()}
#posts = db.posts
#post_id = posts.insert_one(post).inserted_id
#db.list_collection_names()
#import pprint
#pprint.pprint(posts.find_one())
#pprint.pprint(posts.find_one({"author": "Mike"}))
#posts.find_one({"author": "Eliot"})
#pprint.pprint(posts.find_one({"_id": post_id}))


#from pymongo import MongoClient
#client = MongoClient()
#db = client.test_database
#import datetime
#post = {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"], "date": datetime.datetime.utcnow()}
#posts = db.posts
#post_id = posts.insert_one(post).inserted_id
#import pprint
#pprint.pprint(posts.find_one())
#pprint.pprint(posts.find({"author": "Mike"}))
#posts.find_one_and_delete({"author": "Mike"}) #https://www.geeksforgeeks.org/python-mongodb-find_one_and_update-query/
#
#from pymongo import MongoClient
#client = MongoClient()
#db = client.test_database #test_database is the database we store everything in
#db.posts.find_one({"author": "Mike"})
#db.posts.find_one_and_delete({"author": "Mike"})
#db.posts.insert_one({"author": "Mike", "data": "some html code"})
#db.posts.find_one_and_update({"author": "Mike"}, { '$set': {"author":"ed", "data":"some other html code"}})
#db.posts.find_one_and_update({"author": "ed"}, { '$set': {"data":"some new html code"}})
