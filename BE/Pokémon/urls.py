from django.urls import path
from .views import delete_pokemon,add_pokemon, index

urlpatterns = [
    path("list/", index, name="index"), #recupera tutta la lista dei pokemon
    path("", add_pokemon, name="add_pokemon"),  #aggiunge un new pokemon nel db
    path("delete/<int:id>", delete_pokemon, name="delete_pokemon"), #elimina un pokemon 
]