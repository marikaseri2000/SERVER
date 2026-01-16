from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_posts", views.my_posts, name="my_posts"),
]