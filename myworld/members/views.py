from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter

# Create your views here.
# https://www.codingwithricky.com/2019/08/28/easy-django-plotly/
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    from random import randint
    
    x_data = sorted((randint(1,10) for i in range(10)))
    y_data = [x**2 for x in x_data]
    plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines+markers', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div')
    points = list(zip(x_data,y_data))
    return render(request, r"myfirst.html", context={'plot_div': plot_div,
    "points": points})

def room(request, room_name):
    return render(request, r"room.html", {"room_name": room_name})
    #return render(request, r"room.html")