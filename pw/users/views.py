from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import OperationalError, IntegrityError
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import RegisterSerializer

# VISTA PER LA REGISTRAZIONE (ACCESSIBILE A TUTTI)

@api_view(['POST'])
@permission_classes([AllowAny])  # Permettiamo a chiunque di inviare i dati per registrarsi
def register_user(request):
    """
    Crea un nuovo utente e lo collega al profilo partecipante pre-esistente
    """
    try:
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return JsonResponse({
                "username": user.username,
                "message": "Registrazione completata con successo! Ora puoi effettuare il login."
            }, status=status.HTTP_201_CREATED)
            
            # Se i dati non sono validi (es. email non autorizzata o password diverse)
            
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:#OperationalError:
        return Response({'error': str(e)}, status=503)
    except Exception as e:
        return JsonResponse({'error': f'Errore imprevisto: {str(e)}'}, status=500)


# VISTA PER IL PROFILO (SOLO UTENTE LOGGATO)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    Restituisce i dati base dell'utente attualmente loggato tramite Token
    """
    try:
        user = request.user
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin,
            'is_participant': user.is_participant
        }
        return JsonResponse(user_data, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)