from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse, JsonResponse

def index(request):
    return HttpResponse("Hello, world. You're at the comments index.")

def my_comments(request):
    return JsonResponse({
    "postId": 1,
    "id": 5,
    "name": "vero eaque aliquid doloribus et culpa",
    "email": "Hayden@althea.biz",
    "body": "harum non quasi et ratione\ntempore iure ex voluptates in ratione\nharum architecto fugit inventore cupiditate\nvoluptates magni quo et"
  })