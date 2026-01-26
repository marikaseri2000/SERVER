from django.urls import path
from . import views

urlpatterns = [
    path("<projectid:str>/", views.get_task, name="get_task"), 
    path("create/", views.create_task, name="create_task"), 
]