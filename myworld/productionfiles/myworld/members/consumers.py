import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import asyncio
from channels.exceptions import ChannelFull
from pymongo import MongoClient
import re
import ast
from ExecCommunication import ExecCommunication

class ZMQChannels(AsyncWebsocketConsumer):

    def __init__(self):
        super().__init__()
        self.ExecComm = ExecCommunication()

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
        to_do = ast.literal_eval(text_data)
        print('function:', to_do['function'])
        print('instructions:' , to_do['instructions'])
        try:

            # Evaluate to_do: get functionality based on function
            if to_do['function'] == 'signal':
                self.ExecComm.test('signal')
            
            elif to_do['function'] == 'exec_exp':
                # parse instructions?
                params = to_do['instructions']
                self.ExecComm.exec_exp(params)
            
            elif to_do['function'] == 'set_values':
                # parse instructions?
                params = to_do['instructions']
                self.ExecComm.set_values(params)
            
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
                
                #if the user exists
                if db.posts.find_one({"user": user}):
                    db.posts.find_one_and_update({"user": user}, { '$set': {"user": user, "activatedChannels":activatedChannels}})
                #else create the user
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