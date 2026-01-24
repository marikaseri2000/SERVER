from django.db import OperationalError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from task_details.models import TaskDetails
# Create your views here.

@csrf_exempt
@require_http_methods(['PATCH'])
def update_details_project(request, id):
    """
    Aggiorna le notes di un ProjectDetails esistente
    """
    try:
        # Carica i dati dal body JSON
        data = json.loads(request.body)

        # Ottieni il TaskDetails corrispondente
        task_detail = TaskDetails.objects.get(id=id)

        # Aggiorna solo se 'descrizione' è presente nel JSON
        if 'descrizione' in data:
            task_detail.descrizione = data['descrizione']

        task_detail.save()

        return JsonResponse({
            'id': str(task_detail.id),
            'descrizione': task_detail.descrizione,
        }, status=200)

    except TaskDetails.DoesNotExist:
        return JsonResponse({'error': 'Dettaglio progetto non trovato'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON non valido'}, status=400)

    except OperationalError:
        return JsonResponse({'error': 'Database non disponibile'}, status=503)