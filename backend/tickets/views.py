from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .models import Ticket, StatusHistory
from .serializers import (
    TicketSerializer,
    TicketCreateSerializer,
    TicketListSerializer,
    TicketStatusUpdateSerializer,
    UserSerializer,
    RegisterSerializer
)

User = get_user_model()

# -------------------- Auth Views -------------------- #

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Inscription d'un nouvel utilisateur"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'message': 'Utilisateur créé avec succès'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Connexion d'un utilisateur"""
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': "Veuillez fournir un nom d'utilisateur et un mot de passe"},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'message': 'Connexion réussie'
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_view(request):
    """Déconnexion d'un utilisateur"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': 'Token invalide'}, status=status.HTTP_400_BAD_REQUEST)


# -------------------- Ticket ViewSet -------------------- #

class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les tickets
    """
    queryset = Ticket.objects.all().order_by('-created_at')
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        if self.action == 'create':
            return TicketCreateSerializer
        if self.action == 'update_status':
            return TicketStatusUpdateSerializer
        return TicketSerializer

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        """Mettre à jour uniquement le statut du ticket (Admin only)"""
        ticket = self.get_object()
        serializer = TicketStatusUpdateSerializer(instance=ticket, data=request.data)
        serializer.context['request'] = request
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Statut mis à jour avec succès'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
