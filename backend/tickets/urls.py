from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, register_view, login_view, logout_view

# Création du router pour le ViewSet des tickets
router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = [
    # Endpoints d'authentification
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),

    # Endpoints CRUD des tickets via ViewSet
    path('', include(router.urls)),
]
