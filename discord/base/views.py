from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def baseHome(request):
    return HttpResponse("Hello, world. You're at the discord base page.")