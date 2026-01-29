import json
from django.db import IntegrityError, OperationalError
from django.http import JsonResponse
from django.shortcuts import render
from tasks.models import Task
from project.models import Project
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from tag.models import Tag 


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_task(request):
    try:
        data = json.loads(request.body)
        project=Project.objects.filter(user=request.user).get(id=data['project_id'])

        task = Task.objects.create(
            title=data['title'], 
            project=project
        )
        
        return JsonResponse({
            'id': task.id, 
            'title': task.title,
            'project_id': task.project.id,
            'is_complete': task.is_complete
        }, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON non valido'}, status=400)
    
    except KeyError as e:
        return JsonResponse({'error': f'Campo mancante: {e}'}, status=400)
    
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Tipo di dato non valido'}, status=400)
    
    except IntegrityError:
        return JsonResponse({'error': 'Task già esistente'}, status=409)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Progetto non trovato'}, status=404)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_task(request, projectid):
    try:
        tasks = list(Task.objects.filter(project__user_id=request.user, project_id=projectid).values())
        
        return JsonResponse(tasks, safe=False, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON non valido'}, status=400)
    
    except KeyError as e:
        return JsonResponse({'error': f'Campo mancante: {e}'}, status=400)
    
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Tipo di dato non valido'}, status=400)
    
    except IntegrityError:
        return JsonResponse({'error': 'Task già esistente'}, status=409)
    
@csrf_exempt
@require_http_methods(['DELETE'])
def delete_task(request, id):
    try:
        task = Task.objects.get(id=id)
        task.delete()
        
        return JsonResponse(
            {'messaggio': 'Task eliminato'}, 
            status=200)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task non trovato'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(['PATCH'])
def update_details_task(request, id):
    """
    Aggiorna lo stato di un Task esistente
    """
    try:
        # Ottieni il ProjectDetails corrispondente
        task = Task.objects.get(id=id)

        # Aggiorna solo se 'notes' è presente nel JSON
        task.is_complete= not task.is_complete

        task.save()

        return JsonResponse({
            'id': str(task.id),
            'title': task.title,
            'is_complete': task.is_complete,
            'project_id': str(task.project.id),
        }, status=200)

    except Task.DoesNotExist:
        return JsonResponse({'error': 'Dettaglio task non trovato'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON non valido'}, status=400)

    except OperationalError:
        return JsonResponse({'error': 'Database non disponibile'}, status=503)

@csrf_exempt
@require_POST
def add_tag(request):
    try:
        data=json.loads(request.body)
        tag = Tag.objects.get(id=data['tag_id'])
        task = Task.objects.get(id=data['task_id'])
        task.tags.add(tag)
        return JsonResponse({
            'message': 'Tag aggiunto correttamente al Task',
            'task_id': str(task.id),
            'tags': list(task.tags.values('id','name'))
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Json non valido'}, status=400)
    
    # ❌ ID mancanti o non convertibili
    except (KeyError, ValueError, TypeError):
        return JsonResponse(
            {'error': 'tag_id e task_id devono essere numeri validi'},
            status=400
        )

    # ❌ Oggetti non trovati
    except Tag.DoesNotExist:
        return JsonResponse({'error': 'Tag non trovato'}, status=404)

    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task non trovato'}, status=404)

    # ❌ Problemi DB
    except (IntegrityError, OperationalError):
        return JsonResponse(
            {'error': 'Errore del database'},
            status=500
        )

    # ❌ Catch-all (mai lasciare Django esplodere in produzione)
    except Exception as e:
        return JsonResponse(
            {'error': 'Errore interno', 'details': str(e)},
            status=500
        )





