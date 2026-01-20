from django.shortcuts import render
from .models import Pokemon
from django.http import JsonResponse
# Create your views here.

def add_pokemon(request):
    pokemon = Pokemon.objects.create(name="Bulbasaul", pokedex_id=1)
    return JsonResponse({'id': pokemon.id, 'name': pokemon.name, 'pokedex_id': pokemon.pokedex_id})