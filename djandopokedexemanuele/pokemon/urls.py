from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_pokemon_list, name="get_pokemon_list"),
    path("/add", views.add_pokemon, name="add_pokemon"), 
    path("/delete/<str:id>", views.delete_pokemon, name="delete_pokemon"),
    path("/update/patch/<uuid:id>", views.update_pokemon, name="update_pokemon"),
    path("/update/put/<uuid:id>", views.update_put_pokemon, name="update_put_pokemon"),
]