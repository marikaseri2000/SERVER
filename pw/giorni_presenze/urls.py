from . import views
from django.urls import path

urlpatterns = [
    path("", views.manage_giorni, name="manage_giorni"),
]