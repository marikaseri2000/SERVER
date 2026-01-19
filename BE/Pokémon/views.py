from django.shortcuts import render
from .models import Pokemon
from django.http import JsonResponse

def index(request):
    pokemon=Pokemon.objects.all().values()
    print(pokemon)
    return JsonResponse(list(pokemon), safe=False)

def add_pokemon(request):
    pokemon=Pokemon.objects.create(title="Nuovo pokemon", is_available=True) 
    #ci permette di salvare sul bd
    return JsonResponse({"name": pokemon.name, "type": pokemon.type, "level": pokemon.level, "hp": pokemon.hp, "attack": pokemon.attack, "defese": pokemon.defese})

def delete_pokemo(request):

    return JsonResponse()