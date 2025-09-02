from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import RegisterSerializer, UserSerializer
from .models import User
from rest_framework.permissions import AllowAny

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]



from django.http import HttpResponse

def signup_view(request):
    return HttpResponse("Signup page")

def signin_view(request):
    return HttpResponse("Signin page")

def profile_view(request):
    return HttpResponse("Profile page")
