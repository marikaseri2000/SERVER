from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("<uuid:id>/", views.update_details_task, name="update_details_task"),
]