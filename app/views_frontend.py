# app/views_frontend.py
from django.shortcuts import render

from django.shortcuts import render

def home(request):
    api_base = request.build_absolute_uri('/')[:-1] + "/api"
    return render(request, "home.html", {"api_base": api_base})

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')

def notes_list(request):
    return render(request, 'notes_list.html')

def note_new(request):
    return render(request, 'note_edit.html', {'note_id': None})

def note_edit(request, note_id):
    return render(request, 'note_edit.html', {'note_id': str(note_id)})
