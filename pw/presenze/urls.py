from . import views
from django.urls import path

urlpatterns = [
    path("presenza/", views.registra_presenza_singola, name="registra_presenza_singola"),
    path("assenze/<str:partecipante_id>/", views.lista_assenze_partecipante, name="lista_assenze_partecipante"),
    path("<str:giorno_id>/", views.lista_presenze_giorno, name="lista_presenze_giorno"),
]