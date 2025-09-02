"""
URL configuration for app project.
"""
from django.contrib import admin
from django.urls import path, include
from . import views_frontend  # for rendering frontend templates

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Frontend Pages (HTML templates)
    path('', views_frontend.home, name='home'),
    path('signin/', views_frontend.signin, name='signin'),
    path('signup/', views_frontend.signup, name='signup'),
    path('notes/', views_frontend.notes_list, name='notes_list'),
    path('notes/new/', views_frontend.note_new, name='note_new'),
    path('notes/<uuid:note_id>/', views_frontend.note_edit, name='note_edit'),

    # API Endpoints (JSON APIs)
    path('api/users/', include('users.urls')),
    path('api/notes/', include('notes.urls')),
]
