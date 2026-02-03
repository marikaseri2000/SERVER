from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .models import Giorno
from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
    get=extend_schema(
        summary="Calendario lezioni",
        description="Restituisce la lista di tutti i giorni creati",
        tags=["GIORNI"],
        responses={200}
    ),
    post=extend_schema(
        summary="Registrazione giorno",
        description="Crea un nuovo giorno",
        tags=["GIORNI"],
        request=Giorno,
        responses={201}
    ),
)
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def manage_giorni(request):
    """
    Gestione del Calendario Lezioni (Solo Admin).
    
    POST: Crea un nuovo giorno (es. '2026-01-30'). Restituisce l'id_giorno (UUID).
    GET:  Restituisce la lista di tutti i giorni creati.
    """
    
    # 1. Controllo sicurezza: Solo l'Admin può toccare il calendario
    if not request.user.is_admin:
        return JsonResponse({'error': 'Accesso negato: solo admin'}, status=403)

    # --- CREAZIONE NUOVO GIORNO (POST) ---
    if request.method == 'POST':
        try:
            data = request.data
            
            # Creiamo il record nel database
            nuovo_giorno = Giorno.objects.create(
                data=data['data'],  # Formato atteso: YYYY-MM-DD
                descrizione=data.get('descrizione', ''),
                is_active=data.get('is_active', True)
            )
            
            # Restituiamo la data appena creata
            return JsonResponse({
                'message': 'Giorno creato con successo',
                'id_giorno': nuovo_giorno.data, 
                'data': nuovo_giorno.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # Cattura errori (es. se la data esiste già, visto che è unique=True)
            return JsonResponse({'error': str(e)}, status=400)

    # --- LISTA GIORNI ESISTENTI (GET) ---
    if request.method == 'GET':
        # Ordiniamo per data decrescente (dal più recente)
        giorni = Giorno.objects.all().order_by('-data')
        
        lista_giorni = []
        for g in giorni:
            lista_giorni.append({
                'id_giorno': g.data, # Questo ora è la data YYYY-MM-DD
                'data': g.data,
                'descrizione': g.descrizione,
                'is_active': g.is_active
            })
            
        return JsonResponse(lista_giorni, safe=False)