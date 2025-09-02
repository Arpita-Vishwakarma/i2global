# app/views_frontend.py
from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()

def home(request):
    api_base = request.build_absolute_uri('/')[:-1] + "/api"
    return render(request, "home.html", {"api_base": api_base})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()  # ✅ This ensures we use users.User

def signin(request):
    return render(request, "signin.html")


def signup(request):
    if request.method == "POST":
        name = request.POST.get("username")  # or user_name
        email = request.POST.get("email")
        password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")

        # validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        if User.objects.filter(user_email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("signup")

        # ✅ use our custom user manager
        user = User.objects.create_user(
            email=email,
            name=name,
            password=password,
        )
        messages.success(request, "Account created successfully! Please sign in.")
        return redirect("signin")

    return render(request, "signup.html")

def notes_list(request):
    return render(request, 'notes_list.html')

def note_new(request):
    return render(request, 'note_edit.html', {'note_id': None})

def note_edit(request, note_id):
    return render(request, 'note_edit.html', {'note_id': str(note_id)})
