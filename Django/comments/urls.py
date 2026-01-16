from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_comments", views.my_comments, name="my_comments"),
]