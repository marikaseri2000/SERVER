from . import views
from django.urls import path

urlpatterns = [
    path("", views.handle_projects, name="handle_projects"),
    path("<str:id>/", views.delete_project, name="delete_project"),
]