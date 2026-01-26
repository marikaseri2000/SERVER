from django.urls import path
from . import views

urlpatterns = [
    path("<str:projectid>/", views.get_task, name="get_task"), 
    path("create/", views.create_task, name="create_task"),
    path("<str:id>/", views.delete_task, name="delete_task"),
]