from . import views
from django.urls import path

urlpatterns = [
    path("get/", views.manage_participants, name="manage_participants"),
    path("me/", views.get_my_attendance_summary, name="get_my_attendance_summary"),
]