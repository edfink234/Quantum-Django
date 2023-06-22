from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter
from plotly.graph_objects import Heatmap
import plotly.express as px
import csv, json
from multiprocessing import Process, Pool, TimeoutError
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
import asyncio
from pymongo import MongoClient

#views.py: responsible for rendering the html web pages

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
num = 0

def index(request): #Corresponds to myfirst.html
    print(request.user.get_username()) #print username
    client = MongoClient() #instance of a MongoClient
    db = client.test_database #db = the whole mongodb database
    if request.user.is_authenticated:
        username = request.user.username #setting the username
    print(username)
    html_string = ""
    if db.posts.find_one({"user": username}):
        #getting the data of the user if existing already
        html_string = db.posts.find_one({"user": username}).get('index_data') #returns None if index not found in dict
        activated_channels = db.posts.find_one({"user": username}).get('activatedChannels') #returns None if index not found in dict
#        print(activated_channels, type(activated_channels[0]))
    
    #First time: html_string is None
    if not html_string:
        html_string = ""
    print("html_string =",html_string)
    #return the users html (stored in html_string) as a django variable that can be rendered at the bottom of Raman.html
    return render(request, r"myfirst.html", context = {'gui_elements' : html_string, 'channelsActivated' : activated_channels})

def Detection(request):
    return render(request, r"Detection.html")

def Bertha_Channels(request):
    return render(request, r"Bertha_Channels.html")

def Quadrupole(request):
    return render(request, r"Quadrupole.html")

def Motor_Control(request):
    return render(request, r"Motor_Control.html")
    
def Raman(request):
    return render(request, r"Raman.html")

def Static_Control(request):
    return render(request, r"Static_Control.html")


