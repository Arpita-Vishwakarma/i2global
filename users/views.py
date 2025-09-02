from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import SignupSerializer, SigninSerializer
from .models import User
from rest_framework.permissions import AllowAny
from .serializers import SignupSerializer  # ✅ import the correct serializer

class RegisterView(generics.CreateAPIView):
    serializer_class = SignupSerializer




from django.http import HttpResponse

def signup_view(request):
    return HttpResponse("Signup page")

def signin_view(request):
    return HttpResponse("Signin page")

def profile_view(request):
    return HttpResponse("Profile page")



from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer, SigninSerializer, UserSerializer
from .models import User


# Utility: Generate JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "tokens": tokens
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def signin_view(request):
    serializer = SigninSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        tokens = get_tokens_for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "tokens": tokens
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)
