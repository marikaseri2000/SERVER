from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.db import OperationalError, transaction, IntegrityError
import json

from project.models import Project
from project_details.models import ProjectDetails

# Create your views here.

@require_GET
def get_projects_list(request):
    """
    Restituisce la lista di tutti i progetti con i relativi details
    """
    try:
        # select_related usa il nome della relazione OneToOne: 'details'
        projects = Project.objects.select_related('details').all()
        
        projects_list = []
        for project in projects:
            project_data = {
                'id': project.id,
                'name': project.name,
                'details': None
            }
            
            # Controlla se esiste la relazione OneToOne
            if hasattr(project, 'details') and project.details is not None:
                project_data['details'] = {
                    'id': project.details.id,
                    'notes': project.details.notes,
                }
            
            projects_list.append(project_data)
        
        return JsonResponse(projects_list, safe=False)
    
    except OperationalError:
        return JsonResponse({'error': 'Database non disponibile'}, status=503)

@require_POST
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