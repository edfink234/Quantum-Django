import json
from time import sleep
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from random import randint

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

        # Send message to WebSocket
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

class ZMQChannels(WebsocketConsumer):
    count = 0
    def connect(self):
        channel_names.append(self.channel_name)
        print("self.channel_name =",self.channel_name)
        self.room_name = self.scope["url_route"]["kwargs"]
        print(self.room_name)
        
        self.room_group_name = "ZMQ"
        print(self.room_group_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        
        self.groups.append(self.room_group_name)
        
        self.accept()
    def disconnect(self, close_code):
        # Leave room group
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        #pass
    
#    def update(self, message):
#        print("please call!!!")

#    def receive(self, text_data):
#        point_data_json = json.loads(text_data)
#        print("!!!",point_data_json)
#        message = point_data_json["text_data"]
#        # Send message to room group
#        print(message)
#        async_to_sync(self.channel_layer.group_send)(
#            self.room_group_name, {"type": "chat_message", "message": message}
#        )
        
        #self.send(text_data=json.dumps({"message": message}))

    def chat_message(self, event):
        print(event,"!!!")
#        message = event["message"]+"!"*ZMQChannels.count
#        print("message =",message)
#        # Send message to WebSocket
        print("Message here", event["text"])
        self.send(text_data=json.dumps({"event": event}))
        ZMQChannels.count+=1
