from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.db import OperationalError, transaction, IntegrityError
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
from django.views.decorators.http import require_http_methods

from project.models import Project
from project_details.models import ProjectDetails

# Create your views here.

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_projects_list(request):
    """
    Restituisce la lista di tutti i progetti con i relativi details
    """
    print(request.user)
    try:
        # select_related ottimizza la query (un solo JOIN invece di N query)
        projects = Project.objects.filter(user=request.user).select_related('project').all() # SELECT * FROM project;

        projects_list = []
        for project in projects:
            project_data = {
                'id': project.id,
                'name': project.name,
                'details': None
            }

            if hasattr(project, 'project'):
                project_data['details'] = {
                    'id': project.project.id,
                    'notes': project.project.notes,

                }

            projects_list.append(project_data)

        return JsonResponse(projects_list, safe=False)

    except OperationalError:
        return JsonResponse({'error': 'Database non disponibile'}, status=503)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_project(request):
    """
    Aggiunge un nuovo progetto e i relativi details
    """

    try:
        data = json.loads(request.body)

        with transaction.atomic():
            # Crea il progetto
            project = Project.objects.create(
                name=data['name'],
                user=request.user
            )

            # Crea automaticamente i details collegati
            project_details = ProjectDetails.objects.create(
                project=project,
                notes=data.get('notes', ''),
            )

        return JsonResponse({
            'id': project.id,
            'name': project.name,

            'details': {
                'notes': project_details.notes,
            }
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON non valido'}, status=400)

    except KeyError as e:
        return JsonResponse({'errornotesmancante: {e}'}, status=400)

    except IntegrityError:
        return JsonResponse({'error': 'Progetto già esistente'}, status=409)


@csrf_exempt
def handle_projects(request):
    """
    La funzione handle_projects verifica quale metodo tra GET e POST sta ricevendo
    e in base a questo sceglie di eseguire la specifica funzione.

    """
    if request.method == 'GET':
        return get_projects_list(request)
    elif request.method == 'POST':
        return add_project(request)
    else:
        return JsonResponse({'error': 'Metodo non consentito'}, status=405)

@ csrf_exempt
@ require_http_methods(['DELETE'])
def delete_project(request, id):
    try:
        project = Project.objects.get(id=id)
        project.delete()
        return JsonResponse(
            {'messaggio': 'Progetto eliminato'},
            status=200)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Progetto non trovato'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

