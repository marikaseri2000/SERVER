from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse,JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the albums index.")

def my_albums(request):
    return JsonResponse ({
    "userId": 1,
    "id": 5,
    "title": "eaque aut omnis a"
  })