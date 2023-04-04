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

channel_names = []

class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        print(self.room_name)
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        #pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(message*2)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )
#        self.send(text_data=json.dumps({"message": message}))

    def chat_message(self, event):
        message = event["message"]
        print("chat_message",message)
        # Send message to WebSocket
        sleep(1)
        self.send(text_data=json.dumps({"message": message}))

class PlotlyConsumer(WebsocketConsumer):
    max_length = 0;
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]
        # print(self.room_name)
        
        self.room_group_name = "mygroup"
        print(self.room_group_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        #pass

    def receive(self, text_data):
        point_data_json = json.loads(text_data)
        message = point_data_json["text_data"]
        x=list(zip(message[0],message[1]))
        temp = len(str(x));
        if (temp > PlotlyConsumer.max_length):
            PlotlyConsumer.max_length = temp;
        print(" "*PlotlyConsumer.max_length,end="\r",flush=True)
        print(x,flush=True,end="\r")
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )
        
#        self.send(text_data=json.dumps({"message": message}))
    # Receive message from room group
    
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
    
class TestData(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]
        # print(self.room_name)
        
        self.room_group_name = "testdata"
        print(self.room_group_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        
        self.accept()
    def disconnect(self, close_code):
        # Leave room group
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        #pass

    def receive(self, text_data):
        point_data_json = json.loads(text_data)
        message = point_data_json["text_data"]
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )
        
        #self.send(text_data=json.dumps({"message": message}))

    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
    
class TestDataAutomatic(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]
        # print(self.room_name)
        
        self.room_group_name = "testdataAuto"
        print(self.room_group_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        
        self.accept()
    def disconnect(self, close_code):
        # Leave room group
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        #pass

    def receive(self, text_data):
        point_data_json = json.loads(text_data)
        message = point_data_json["text_data"]
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

class ZMQChannels(AsyncWebsocketConsumer):
    count = 0
    consumers = 0
#    channel_layer = get_channel_layer()
    tasks = []
    async def connect(self):
#        global obj_list
        channel_names.append(self.channel_name)
        print("self.channel_name =",self.channel_name)
        self.room_name = self.scope["url_route"]["kwargs"]
        print(self.room_name)
        self.room_group_name = "ZMQ"
        print(self.room_group_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        
        self.groups.append(self.room_group_name)
        self.consumer = ZMQChannels.consumers
        await self.accept()
        ZMQChannels.consumers += 1
    async def disconnect(self, close_code):
        # Leave room group
        print('disconnecting')
        ZMQChannels.consumers-=1
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
    
    #Receives data from Raman.html and sends it to server.py
    async def receive(self, text_data):
#        print(self.scope["user"])
#        print(text_data)
        try:
            await self.channel_layer.send("ZMQ", {"type": "chat.message", "text_data":json.dumps(text_data)})
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
