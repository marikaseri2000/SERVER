from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from .data import user_list #con il punto va dentro alla cartella

def index(request):
    return HttpResponse("Hello, world. You're at the users index.")
def my_users(request):
    #rendiamo il risultato dinamico in base a quello che vogliamo ricedere, 
    #in questo caso vogliamo visualizzare il primo diz
    return JsonResponse(user_list[0], safe=False)


def user(request, id):
    """funzione dinamica in cui l'id viene scelto """
    user= next((u for u in user_list if u.get("id") == id), None)
    #user= next(u for u in user_list if u.get("id) == {5}, None)
    #così se mettiamo qui l'id specifico
    if user is None: 
        return JsonResponse ({"errore": "User not found"}, status=404)
    return JsonResponse(user, safe= False)
    