from . import views
from django.urls import path

urlpatterns = [
    path("crea_spesa/", views.crea_spesa, name="crea_spesa"),
    path("spese_categoria/<str:id>/", views.spese_per_categorie, name="spese_per_categorie"),
    path("spese_mese/", views.spese_mese, name="spese_mese"),
    path("budget_residuo_categoria/<str:id>/", views.budget_residuo_categoria, name="budget_residuo_categoria"),
    path("totale_spese_categoria/<str:id>/", views.totale_spese_categoria, name="totale_spese_categoria"),
    path("dettaglio_spesa/<str:id>/", views.dettagli_spesa, name="dettagli_spesa"),
    path("aggiorna_spesa/<str:id>/", views.modifica_spesa, name="modifica_spesa"),
    path("elimina_spesa/<str:id>/", views.elimina_spesa, name="elimina_spesa"),
]