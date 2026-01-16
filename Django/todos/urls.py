from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_todos/", views.my_todos, name="my_todos"),
]