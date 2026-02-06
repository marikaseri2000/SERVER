from . import views
from django.urls import path

urlpatterns = [
    path("add_categoria/", views.crea_categoria, name="crea_categoria"),
    path("all_categorie/", views.lista_categorie, name="lista_categorie"),
    path("dettaglio_cat/<str:id>/", views.dettagli_categoria, name="dettagli_categoria"),
    path("aggiorna_cat/<str:id>/", views.modifica_categoria, name="modifica_categoria"),
    path("elimina_cat/<str:id>/", views.elimina_categoria, name="elimina_categoria"),
]