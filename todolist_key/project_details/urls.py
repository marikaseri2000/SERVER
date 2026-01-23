from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("<str:id>/", views.update_details_project, name="update_details_project"),
]