from django.shortcuts import render
from .models import Room
# Create your views here.

# rooms = [
#     {'id':1, 'name':'Python', 'description':'This is room 1'},
#     {'id':2, 'name':'JS', 'description':'This is room 2'},
#     {'id':3, 'name':'SQL', 'description':'This is room 3'},

# ]

def home(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request, 'base/home.html', context)

# def home(request):
#     return render(request, 'home.html', {'rooms':rooms})

def room(request, pk):

    room = Room.objects.get(id = pk)
            
    context = {'room':room}
    return render(request, 'base/room.html', context)