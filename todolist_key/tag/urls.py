from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_tag, name="create_tag"),
    path("", views.get_tags, name="get_tags"),
    path("<str:task_id>/", views.get_tags_by_id, name="get_tags_by_id"),
]