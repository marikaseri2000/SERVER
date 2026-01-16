from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the photos index.")

def my_photos(request):
    return JsonResponse({
    "albumId": 1,
    "id": 5,
    "title": "natus nisi omnis corporis facere molestiae rerum in",
    "url": "https://via.placeholder.com/600/f66b97",
    "thumbnailUrl": "https://via.placeholder.com/150/f66b97"
  })