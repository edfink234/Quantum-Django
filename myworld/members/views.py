from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter
from plotly.graph_objects import Heatmap
import plotly.express as px
import csv, json



# Create your views here.
# https://www.codingwithricky.com/2019/08/28/easy-django-plotly/
from django.shortcuts import render
from django.http import HttpResponse

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



def data_room(request):
    import pandas as pd
    full_df = pd.read_csv("members/0_data_decrystallized_noIon.csv", header = None)
    df = full_df.iloc[:,1:]
#    df_col = full_df.iloc[:,1]
#    df_html = df#.to_html()
    context = {'loaded_data': full_df, 'string_loaded_data': df.to_string(header=None, index = False)}
    return render(request, r"mysecond.html", context)

def index(request):
    from random import randint
    
    x_data = sorted((randint(1,10) for i in range(10)))
    y_data = [x**2 for x in x_data]
    plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines+markers', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div')
    points = list(zip(x_data,y_data))
    with open("members/0_data_decrystallized_noIon.csv") as f:
        reader = csv.reader(f)
        row1 = next(reader)
    import numpy as np
    row1 = [int(i) for i in row1[2:]]
    x = np.array(row1).reshape((11,11))
    fig_div = plot([Heatmap(z = x, type = 'heatmap')],
               output_type='div')
    
    return render(request, r"myfirst.html", context={'plot_div': plot_div,
    "points": points, 'fig_div' : fig_div})

def room(request, room_name):
    return render(request, r"room.html", {"room_name": room_name})
    #return render(request, r"room.html")
