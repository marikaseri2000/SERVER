from django.db import IntegrityError, OperationalError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from project_details.models import ProjectDetails

@csrf_exempt
@require_http_methods(['PATCH'])
def update_details_project(request, id):
    """
    Aggiorna le notes di un ProjectDetails esistente
    """
    try:
        # Carica i dati dal body JSON
        data = json.loads(request.body)

        # Ottieni il ProjectDetails corrispondente
        project_detail = ProjectDetails.objects.get(id=id)

        # Aggiorna solo se 'notes' è presente nel JSON
        if 'notes' in data:
            project_detail.notes = data['notes']

        project_detail.save()

        return JsonResponse({
            'id': str(project_detail.id),
            'notes': project_detail.notes,
        }, status=200)

    except ProjectDetails.DoesNotExist:
        return JsonResponse({'error': 'Dettaglio progetto non trovato'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON non valido'}, status=400)

    except OperationalError:
        return JsonResponse({'error': 'Database non disponibile'}, status=503)