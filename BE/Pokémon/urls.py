from django.urls import path

from . import views

urlpatterns = [
    path("pokemon/list", views.index, name="index"), #recupera tutta la lista dei pokemon
    path("pokemon/", views.add_pokemon, name="add_pokemon"),  #aggiunge un new pokemon nel db
    path("pokemon/delete", views.delete_pokemon, name="delete_pokemon") #elimina un pokemon 
]