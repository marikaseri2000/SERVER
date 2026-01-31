from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

from .models import Presenza
from partecipanti.models import Partecipante
from giorni_presenze.models import Giorno

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def registra_presenza_singola(request):
    """
    L'admin invia i dati per segnare la presenza di uno studente.
    Esempio JSON: 
    {
        "giorno_id": "uuid-del-giorno",
        "partecipante_id": "uuid-matricola",
        "stato": true
    }
    """
    # Verifichiamo che sia l'admin a parlare
    if not request.user.is_admin:
        return JsonResponse({'error': 'Solo l\'admin può segnare le presenze'}, status=403)

    try:
        data = request.data
        
        # Creiamo o aggiorniamo la presenza (così se l'admin sbaglia può correggere)
        presenza, created = Presenza.objects.update_or_create(
            giorno_id=data['giorno_id'],
            partecipante_id=data['partecipante_id'],
            defaults={'stato': data.get('stato', True)}
        )

        return JsonResponse({
            'message': 'Presenza salvata con successo',
            'nuovo_record': created,
            'stato_finale': presenza.stato
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def lista_presenze_giorno(request, giorno_id):
    """
    Restituisce l'elenco di tutti quelli che erano presenti in un giorno specifico
    """
    if not request.user.is_admin:
        return JsonResponse({'error': 'Accesso negato'}, status=403)

    presenze = Presenza.objects.filter(id_giorno=giorno_id, stato=True).select_related('partecipante')
    
    risultato = []
    for p in presenze:
        risultato.append({
            'matricola': p.partecipante.matricola,
            'nome': p.partecipante.user.username if p.partecipante.user else "Account non registrato"
        })
        
    return JsonResponse(risultato, safe=False)