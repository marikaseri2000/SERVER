import json
from django.db import OperationalError
from django.http import JsonResponse
from django.shortcuts import render
from tag.models import Tag
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Create your views here.
@csrf_exempt
@require_POST
def create_tag(request):
    try:
        data=json.loads(request.body)
        tag = Tag.objects.create(
            name=data['name']
        )
        return JsonResponse({
            'id': tag.id,
            'name': tag.name
        }, status=201)
    
    except Tag.DoesNotExist:
        return JsonResponse({'error': 'Dettaglio tag non trovato'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON non valido'}, status=400)

    except OperationalError:
        return JsonResponse({'error': 'Database non disponibile'}, status=503)
    
