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
        
        #self.send(text_data=json.dumps({"message": message}))

    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

obj_list = []
async def ZMQChannels_send(event):
    global obj_list
    print(len(obj_list))
    tasks = []
    for i in obj_list:
        tasks.append(asyncio.create_task(i.send(text_data=json.dumps({"event": event}))))
    if not tasks:
        return
    done, pending = await asyncio.wait(tasks)
    obj_list.clear()

def append_to_obj_list(obj):
    global obj_list
    obj_list.append(obj)

class ZMQChannels(AsyncWebsocketConsumer):
    count = 0
    consumers = 0
#    channel_layer = get_channel_layer()
    tasks = []
    async def connect(self):
        global obj_list
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
        append_to_obj_list(self)
    async def disconnect(self, close_code):
        # Leave room group
        print('disconnecting')
        ZMQChannels.consumers-=1
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        #pass
    async def receive(self, text_data):
#        channel_layer = get_channel_layer()
#        print(text_data)
#        print(channel_layer)
#        sleep(0.1)
        try:
            await self.channel_layer.send("ZMQ", {"type": "chat.message", "text_data":json.dumps(text_data)})
        except ChannelFull:
#            print("caught!")
            pass
#            sleep(0.1)
#            sys.exit(1)
            
#        await ZMQChannels.channel_layer.send("ZMQ", {"type": "chat.message", "text_data":json.dumps(text_data)})
        
    async def chat_message(self, event):
#        print(event,"!!!")
#        sleep(1)
#        message = event["message"]+"!"*ZMQChannels.count
#        print("message =",message)
#        # Send message to WebSocket
        
#        print("Message received from consumers!", event["text"])
#        await self.channel_layer.group_send("ZMQ", {"type": "chat.message", "text_data":json.dumps({"event": event})})
#        ZMQChannels.count += 1
#        if ZMQChannels.count == ZMQChannels.consumers:

#        ZMQChannels.count+=1
#        print(ZMQChannels.consumers,ZMQChannels.count)
#        ZMQChannels.tasks.append(asyncio.create_task(self.send(text_data=json.dumps({"event": event}))))
#        if ZMQChannels.count == ZMQChannels.consumers:
#            done, pending = await asyncio.wait(ZMQChannels.tasks)
##            await ZMQChannels_send(event)
#            ZMQChannels.tasks.clear()
#            ZMQChannels.count = 0
            
            
        await self.send(text_data=json.dumps({"event": event}))
#        await self.send(text_data=json.dumps({"event": event}))

#            await ZMQChannels.channel_layer.group_send("ZMQ", {"type": "chat.message", "text_data":json.dumps({"event": event})})
#            ZMQChannels.count = 0
#        ZMQChannels.count+=1
