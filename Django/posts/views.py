from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the posts index.")

def my_posts(request):
    return JsonResponse({
    "userId": 1,
    "id": 6,
    "title": "dolorem eum magni eos aperiam quia",
    "body": "ut aspernatur corporis harum nihil quis provident sequi\nmollitia nobis aliquid molestiae\nperspiciatis et ea nemo ab reprehenderit accusantium quas\nvoluptate dolores velit et doloremque molestiae"
  })