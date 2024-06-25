from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, world. You're at the discord home page.")

def about(request):
    return HttpResponse("about page of the discord")