from django.db import OperationalError
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from .models import Partecipante
from giorni_presenze.models import Giorno
from presenze.models import Presenza
from partecipanti.serializers import ParticipantAdminSerializer # Assicurati di averlo creato!
from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    get=extend_schema(
        summary="Elenco partecipanti",
        description="Restituisce la lista dei partecipanti (esclusi gli admin)",
        tags=["PARTECIPANTI"],
        responses={200: ParticipantAdminSerializer(many=True)},
    ),
    post=extend_schema(
        summary="Registrazione partecipante",
        description="Crea un nuovo partecipante",
        tags=["PARTECIPANTI"],
        request=ParticipantAdminSerializer,
        responses={201: ParticipantAdminSerializer},
    ),
)
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def manage_participants(request):
    if not request.user.is_admin:
        return JsonResponse({'error': 'Solo l\'admin può gestire i partecipanti'}, status=403)

    if request.method == 'GET':
        # Escludiamo gli admin dalla lista dei partecipanti
        partecipanti = Partecipante.objects.exclude(user__is_admin=True)
        serializer = ParticipantAdminSerializer(partecipanti, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        serializer = ParticipantAdminSerializer(data=request.data)
        if serializer.is_valid():
            # QUESTO SALVA NEL DATABASE (DBeaver vedrà i dati)
            serializer.save() 
        return JsonResponse(serializer.data, status=201)
        
    return JsonResponse(serializer.errors, status=400)


@extend_schema(
    summary="Riepilogo dati partecipante (admin)",
    description="Permette all'admin di vedere il riepilogo di un partecipante specifico tramite ID",
    tags=["PARTECIPANTI"],
    request=ParticipantAdminSerializer,
    responses={200}
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_participant_summary_admin(request, partecipante_id):
    """
    Permette all'admin di vedere il riepilogo di un partecipante specifico tramite ID
    """
    if not request.user.is_admin:
        return JsonResponse({'error': 'Solo l\'admin può vedere i riepiloghi altrui'}, status=403)

    try:
        # Recuperiamo il partecipante tramite ID (matricola)
        partecipante = Partecipante.objects.get(matricola=partecipante_id)

        # Contiamo i giorni totali
        giorni_totali = Giorno.objects.count()

        # Contiamo le presenze effettive
        presenze_effettive = Presenza.objects.filter(
            partecipante=partecipante, 
            stato=True
        ).count()

        percentuale = (presenze_effettive / giorni_totali * 100) if giorni_totali > 0 else 0

        return JsonResponse({
            'matricola': partecipante.matricola,
            'email': partecipante.email_preautorizzata,
            'dati_frequenza': {
                'lezioni_totali': giorni_totali,
                'presenze_confermate': presenze_effettive,
                'percentuale': f"{round(percentuale, 2)}%",
                'obiettivo_80_percento': percentuale >= 80
            }
        }, status=status.HTTP_200_OK)

    except Partecipante.DoesNotExist:
        return JsonResponse({'error': 'Partecipante non trovato'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# VISTA DEI PARTECIPANTI
@extend_schema(
    summary="Statistiche delle presenze",
    description="Calcola la percentuale basata sui giorni totali e le presenze effettive",
    tags=["PARTECIPANTI"],
    request=ParticipantAdminSerializer,
    responses={200}
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_my_attendance_summary(request):
    """
    Calcola la percentuale basata sui giorni totali e le presenze effettive
    """
    try:
        # 1. Recuperiamo il partecipante collegato all'utente loggato
        partecipante = Partecipante.objects.get(user=request.user)

        #Contiamo quanti giorni di lezione totali esistono nel database
        giorni_totali = Giorno.objects.count()

        #Contiamo quante volte il partecipante è segnato con stato=True
        presenze_effettive = Presenza.objects.filter(
            partecipante=partecipante, 
            stato=True
        ).count()

#Calcolo percentuale dinamico
        percentuale = (presenze_effettive / giorni_totali * 100) if giorni_totali > 0 else 0

        return JsonResponse({
            'matricola': partecipante.matricola,
            'username': request.user.username,
            'dati_frequenza': {
                'lezioni_totali': giorni_totali,
                'presenze_confermate': presenze_effettive,
                'percentuale': f"{round(percentuale, 2)}%",
                'obiettivo_80_percento': percentuale >= 80
            }
        }, status=status.HTTP_200_OK)

    except Partecipante.DoesNotExist:
        return JsonResponse({'error': 'Profilo non trovato'}, status=404)
    except OperationalError:
        return JsonResponse({'error': 'Database non raggiungibile'}, status=503)
    