from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_photos/", views.my_photos, name="my_photos"),
]