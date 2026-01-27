from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_task, name="create_task"),
    path("add-tag/", views.add_tag, name="add_tag"),
    path("project/<str:projectid>/", views.get_task, name="get_task"),
    path("delete/<str:id>/", views.delete_task, name="delete_task"),
    path("update/<str:id>/", views.update_details_task, name="update_details_task"),
]