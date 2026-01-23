from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import transaction, IntegrityError
import json

from project.models import Project
from project_details.models import ProjectDetails

# Create your views here.

def get_projects_list(request):
    """
    Restituisce la lista di tutti i progetti che ci sono nel DB.
    
    """
    pass

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