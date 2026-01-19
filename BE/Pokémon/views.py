from django.shortcuts import render
from .models import Pokemon
from django.http import JsonResponse, HttpResponseNotAllowed

def index(request):
    pokemon=Pokemon.objects.all().values()
    print(pokemon)
    return JsonResponse(list(pokemon), safe=False)

def add_pokemon(request):
    pokemon=Pokemon.objects.create(name="Nuovo pokemon", type="sisha") 
    #ci permette di salvare sul bd
    return JsonResponse({"id": pokemon.id, "name": pokemon.name, "type": pokemon.type})

def delete_pokemon(request, id):
    if request.method not in ["DELETE", "GET"]:
        return HttpResponseNotAllowed(["DELETE"])

    try:
        pokemon = Pokemon.objects.get(id=id)
        pokemon.delete()
        
        return JsonResponse(
            {"message": "Pokemon con id:{} eliminato con successo!!".format(id)},
            status=200
        )

    except Pokemon.DoesNotExist:
        return JsonResponse(
            {"errore": "Pokemon not found"},
            status=404
        )

