from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Authentication API
    path('signup/', views.signup_view, name='signup'),   # user registration
    path('signin/', views.signin_view, name='signin'),   # user login
    path('profile/', views.profile_view, name='profile'),

    # JWT Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
