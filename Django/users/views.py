from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the users index.")
def my_users(request):
    return JsonResponse({
    "phone": "493-170-9623 x156",
    "website": "kale.biz",
    "company": {
      "name": "Robel-Corkery",
      "catchPhrase": "Multi-tiered zero tolerance productivity",
      "bs": "transition cutting-edge web services"
    }}
    )