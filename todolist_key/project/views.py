import json
from django.db import IntegrityError, OperationalError
from django.http import JsonResponse
from django.shortcuts import render
from project.models import Project
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Create your views here.
@csrf_exempt 
@require_POST
def add_task(request):
    try:
        data = json.loads(request.body)
        
        task = Project.objects.create(
            nome=
            descrizione=
            status=
            
            titolo=data['titolo'], 
            descrizione=data['descrizione'],
            data_creazione=data['data_creazione'],
            data_modifica=data['data_modifica'],
            data_completamento=data['data_completamento'],
        )
        
        return JsonResponse({
            'id': task.id, 
            'titolo': task.titolo, 
            'descrizione': task.descrizione,
            'data_creazione': task.data_creazione,
            'data_modifica': task.data_modifica,
            'data_completamento': task.data_completamento,
        }, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON non valido'}, status=400)
    
    except KeyError as e:
        return JsonResponse({'error': f'Campo mancante: {e}'}, status=400)
    
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Tipo di dato non valido'}, status=400)
    
    except IntegrityError:
        return JsonResponse({'error': 'Project già esistente'}, status=409)
    
    except OperationalError:
        return JsonResponse({'error': 'Database non disponibile'}, status=503)
    
    except Exception as e:
        return JsonResponse({'error': 'Errore interno del server'}, status=500)
