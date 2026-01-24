import json
from django.db import IntegrityError, OperationalError
from django.http import JsonResponse
from django.shortcuts import render
from .models import Task
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# Create your views here.

@csrf_exempt 
@require_POST
def add_task(request, id):
    try:
        data = json.loads(request.body)
        task = Task.objects.create(
            name=data['name'], 
            descrizione=data['descrizione'],
        )
        
        return JsonResponse({
            'id': task.id, 
            'name': task.name, 
            'descrizione': task.descrizione,
        }, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON non valido'}, status=400)
    
    except KeyError as e:
        return JsonResponse({'error': f'Campo mancante: {e}'}, status=400)
    
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Tipo di dato non valido'}, status=400)
    
    except IntegrityError:
        return JsonResponse({'error': 'Task già esistente'}, status=409)
    
    except OperationalError:
        return JsonResponse({'error': 'Database non disponibile'}, status=503)
    
    except Exception as e:
        return JsonResponse({'error': 'Errore interno del server'}, status=500)
