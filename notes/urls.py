from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet

# DRF Router for Notes CRUD
router = DefaultRouter()
router.register(r'', NoteViewSet, basename='note')

urlpatterns = [
    # Include the automatically generated routes for NoteViewSet
    path('', include(router.urls)),
]
