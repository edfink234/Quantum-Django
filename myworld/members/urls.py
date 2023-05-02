from django.urls import path
from . import views

#matches different views functions (from views.py) to file paths.
#For example, the path Detection/Detection/ will call the Detection function in views.py
#to render the html of that path (Detection.html)

urlpatterns = [path("", views.index, name="index"), 
path("Detection/Detection/", views.Detection, name = "Detection"),
path("Bertha_Channels/Bertha_Channels/", views.Bertha_Channels, name = "Bertha_Channels"),
path("Motor_Control/Motor_Control/", views.Motor_Control, name = "Motor_Control"),
path("Quadrupole/Quadrupole/", views.Quadrupole, name = "Quadrupole"),
path("Raman/Raman/", views.Raman, name = "Raman"),
path("Static_Control/Static_Control/", views.Static_Control, name = "Static_Control"),
]
