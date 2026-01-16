from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse, JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the todos index.")
def my_todos(request):
    return JsonResponse({
    "userId": 1,
    "id": 5,
    "title": "laboriosam mollitia et enim quasi adipisci quia provident illum",
    "completed": False
  })