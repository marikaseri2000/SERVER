from . import views
from django.urls import path

urlpatterns = [
    path("preautorizzazione/", views.manage_participants, name="manage_participants"),
    path("me/", views.get_my_attendance_summary, name="get_my_attendance_summary"),
    path("summary/<str:partecipante_id>/", views.get_participant_summary_admin, name="get_participant_summary_admin"),
]