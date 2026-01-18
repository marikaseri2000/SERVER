from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_urls/", views.my_urls, name="my_urls"),
    path("<int:id>", views.user, name="user"),
]