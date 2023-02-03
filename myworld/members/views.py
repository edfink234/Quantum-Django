from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter
from plotly.graph_objects import Heatmap
import plotly.express as px
import csv, json
from multiprocessing import Process
#import zmq
from itertools import cycle #cycle through data
from time import sleep
# Create your views here.
# https://www.codingwithricky.com/2019/08/28/easy-django-plotly/
from django.shortcuts import render
from django.http import HttpResponse
#https://stackoverflow.com/questions/58832526/is-it-possible-to-use-zeromq-sockets-in-a-django-channels-consumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import zmq
import subprocess
import sys
import os

'''
0_data_decrystallized_noIon.csv
===============================
Min: 407, 0.0
Max: 1094, 5.7

1_data_crystallized_oneIon.csv
==============================
Min: 417, 36.3
Max: 1518, 61.8

2_data_crystallized_two_ions.csv
================================
Min: 420, 63.5
Max: 1497, 92.7

3_data_decrystallized_hot.csv
=============================
Min: 412, 27.0
Max: 1253, 77.7

4_data_decrystallized_cloud.csv
===============================
Min: 415, 191.2
Max: 1349, 227.7

All
===
Min: 407, 0.0
Max: 1518, 227.7
'''

loaded = False

ZMQ_server_loaded = False
ZMQ_client_loaded = False
ZMQ_server_context = None
socket = None

num = 0

#kill -9 `ps -ef | grep python | awk '{print $2}' | xargs`
#TODO: Change REQ to pub/sub as in Melzer Christian's example

def clientZMQ():
    ZMQ_client_context = zmq.Context()
    print("Connecting to hello world server…")
    client_socket = ZMQ_client_context.socket(zmq.REQ)
    print("🥹")
    client_socket.connect("tcp://localhost:5555")
    print("😓")
    try:
        for request in cycle(range(100)):
            print("Sending request %s …" % request)
            client_socket.send_string("Hello "+str(request))
            sleep(1)
            #  Get the reply.
            message = client_socket.recv()
            print("Received reply %s [ %s ]" % (request, message))
    finally:
        client_socket.disconnect("tcp://localhost:5555")
        ZMQ_client_context.term()
      
def serverZMQ():
    global ZMQ_server_loaded, ZMQ_server_context, socket
    try:
        if not ZMQ_server_loaded:
            ZMQ_server_context = zmq.Context()
            socket = ZMQ_server_context.socket(zmq.REP)
            print("🤯")
            sleep(1)
            socket.bind("tcp://*:5555")
            print("here")
            ZMQ_server_loaded = True
    #
        print("🥳")
        channel_layer = get_channel_layer()
        print("Here is the ",channel_layer)
        
        #TODO: connect to client 1 time via socket.bind, get message, and send it below instead of "announcement_text". Then commit to Git!!!
        #
        for request in cycle(range(100)):
            message = socket.recv()
            print("server got", message)
            socket.send_string("World")
            sleep(1)
            async_to_sync(channel_layer.group_send)(
                "ZMQ",
                {"type": "chat.message", "text": request},
            )
    #        await channel_layer.group_send("ZMQ",
    #            {"type": "chat.message", "text": request},
    #        )
    except:
        sys.exit()
    finally:
#        print("ZMQ died")
        ZMQ_server_context.term()


def TrueClientZMQ():
    ZMQ_client_context = zmq.Context()
    print("Connecting to hello world server…")
    client_socket = ZMQ_client_context.socket(zmq.PUB)
    print("🥹")
    client_socket.bind("tcp://*:7539")
    print("😓")
    try:
        for request in cycle(range(100)):
            print("Sending request %s …" % request)
            client_socket.send_multipart([b"CAMERA", request])
            sleep(1)
            #  Get the reply.
    finally:
        ZMQ_client_context.term()
      
def TrueServerZMQ():
    global ZMQ_server_loaded, ZMQ_server_context, socket
    try:
        if not ZMQ_server_loaded:
            ZMQ_server_context = zmq.Context()
            socket = ZMQ_server_context.socket(zmq.SUB)
            print("🤯")
            sleep(1)
            socket.connect("tcp://localhost:7539")
            print("here")
            ZMQ_server_loaded = True
            socket.setsockopt(zmq.SUBSCRIBE, b"CAMERA")
    #
        print("🥳")
        channel_layer = get_channel_layer()
        print("Here is the ",channel_layer)
        
        #TODO: connect to client 1 time via socket.bind, get message, and send it below instead of "announcement_text". Then commit to Git!!!
        #
        for request in cycle(range(100)):
            message = socket.recv()
            print("server got", message)
            sleep(1)
            async_to_sync(channel_layer.group_send)(
                "ZMQ",
                {"type": "chat.message", "text": request},
            )
    #        await channel_layer.group_send("ZMQ",
    #            {"type": "chat.message", "text": request},
    #        )
    except:
        sys.exit()
    finally:
#        print("ZMQ died")
        socket.disconnect("tcp://localhost:7539")
        ZMQ_server_context.term()
    
def data_room(request):
    import pandas as pd
    full_df = pd.read_csv("members/0_data_decrystallized_noIon.csv", header = None)
    df = full_df.iloc[:,1:]
#    df_col = full_df.iloc[:,1]
#    df_html = df#.to_html()
    context = {'loaded_data': full_df, 'string_loaded_data': df.to_string(header=None, index = False)}
    return render(request, r"mysecond.html", context)

def index(request):
    import pandas as pd
    full_df = pd.read_csv("members/0_data_decrystallized_noIon.csv", header = None)
    df = full_df.iloc[:,1:]
    context = {'loaded_data': full_df, 'string_loaded_data': df.to_string(header=None, index = False)}
    return render(request, r"myfirst.html", context)

def Detection(request):
    from random import randint
    
    x_data = sorted((randint(1,10) for i in range(10)))
    y_data = [x**2 for x in x_data]
    plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines+markers', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div')
    points = list(zip(x_data,y_data))
    return render(request, r"Detection.html", context={'plot_div': plot_div,
    "points": points})

def Bertha_Channels(request):
    global loaded, num
    print("again")
    if not loaded:
        subprocess.Popen(["python3", "serverZMQ.py", f"{num}"])
        subprocess.Popen(["python3", "clientZMQ.py", f"{num}"])
        num+=1
#        loaded = True
    with open("members/0_data_decrystallized_noIon.csv") as f:
        reader = csv.reader(f)
        row1 = next(reader)
    import numpy as np
    row1 = [int(i) for i in row1[2:]]
    x = np.array(row1).reshape((11,11))
    fig_div = plot([Heatmap(z = x, type = 'heatmap')],
               output_type='div')
    return render(request, r"Bertha_Channels.html", context={'fig_div' : fig_div, "string_loaded_data" : num})

def Quadrupole(request):
    return render(request, r"Quadrupole.html")

def Motor_Control(request):
    return render(request, r"Motor_Control.html")

def room(request, room_name):
    return render(request, r"room.html", {"room_name": room_name})
    #return render(request, r"room.html")

def Raman(request):
    global ZMQ_client_loaded
    p1 = Process(target=serverZMQ)
#    p1 = Process(target=TrueClientZMQ)
    p1.start()
#    subprocess.Popen(["python3", "serverZMQtest.py"])
    if not ZMQ_client_loaded:
#        subprocess.Popen(["python3", "clientZMQtest.py"])
        p = Process(target=clientZMQ)
#        p = Process(target = TrueServerZMQ)
        ZMQ_client_loaded = True
        
        p.start()
#        subprocess.Popen(["python3", "serverZMQtest.py"])
#    p1.start()
    return render(request, r"Raman.html")

def Static_Control(request):
    return render(request, r"Static_Control.html")

