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
    activated_channels = []
    
    user_db = db.posts.find_one({"user": username})
    
#    Uncomment the following two lines to delete the current user and test it again
#    db.posts.find_one_and_delete({"user": username})
#    user_db = db.posts.find_one({"user": username})
    
    if user_db == None:
        db.posts.insert_one({"user": username})
        user_db = db.posts.find_one({"user": username})
    #getting the data of the user if existing already
    if user_db.get('index_data') == None:
        db.posts.find_one_and_update({"user": username}, { '$set': {"index_data": ""}})

    if user_db.get('activatedChannels') == None:
        db.posts.find_one_and_update({"user": username}, { '$set': {"activatedChannels": [True]*16}})

    functionDict = {'729Spec': {'params' : {'startFreq': {'type': 'float', 'default': 10.0, 'info': 'Defines the start frequency of the measurement.'},
             'stopFreq': {'type': 'float', 'default': 20.0, 'info': 'Defines the stop fequency of the measurement.'},
             'stepSize': {'type': 'float', 'default': 2, 'info': 'Defines the step size between two measurement points.'},
             'quenchAfter': {'type': 'bool', 'default': True, 'info': 'If True, quenches after measurement is completed.'}
            },
            'description' : 'This Experiment does 729 Spectroscopy.',
            'other_metadata' : []
            } ,
            '729ShelvingTest' : {'params' : { 'Location': {'type': 'str', 'default': '', 'info': 'Location of Shelving Test.'}
                  },
               'description' : 'This Experiment does a 729 Shelving Test.',
            'other_metadata' : []
            } ,
            'RamanCalibrationScan' : {'params' : { 'piTime': {'type': 'float', 'default': 1.0e-5, 'info': 'Pi pulse duration.'},
                    'repetitions': {'type': 'int', 'default': 1, 'info': 'Amount of times the Scan is repeated.'},
                },
            'description' : 'This Experiment does a Raman Calibration Scan.',
               'other_metadata' : []
               },
            'MeasureBeamProfile' : {'params' : {} ,
            'description' : 'This Experiment measures the Beam Profile.',
             'other_metadata' : []
            }
        }
    
    if user_db.get("functionDict") == None:
        db.posts.find_one_and_update({"user": username}, { '$set': {"functionDict": functionDict}})
    
    possibleHTMLelements = {"users_html": {"status":True, "html": "<div class=\"col-sm\" id = 'users_html'> gui_elements </div>"}, "dropdownMenuButtonChanOutput": {"status":True}, "dropdownMenuButtonSetFreqAmplChanPhaseOutput": {"status":True}, "Signal": {"status":True}, "Stop": {"status":True}, "Start": {"status":True}, "time_diff": {"status":True}, "voltages": {"status":True}, "heat-map-line-graph-show": {"status":True}}
    
    #return the users html (stored in html_string) as a django variable that can be rendered at the bottom of Raman.html
    return render(request, r"myfirst.html", context = {'gui_elements' : user_db.get('index_data'), 'channelsActivated' : json.dumps(user_db.get('activatedChannels')), 'functionDict' : json.dumps(user_db.get("functionDict")), 'possibleHTMLelements': json.dumps(possibleHTMLelements)})

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


