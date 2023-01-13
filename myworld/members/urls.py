from django.urls import path
from . import views

urlpatterns = [path("", views.index, name="index"), 
path("<str:room_name>/", views.room, name="room"),
path("data/data/", views.data_room, name = "data"),
path("Detection/Detection/", views.Detection, name = "Detection"),
path("Bertha_Channels/Bertha_Channels/", views.Bertha_Channels, name = "Bertha_Channels"),
path("Motor_Control/Motor_Control/", views.Motor_Control, name = "Motor_Control"),

]
