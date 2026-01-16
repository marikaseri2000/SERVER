from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_albums/", views.my_albums, name="my_albums"),
]