from rest_framework import serializers
from .models import Ticket, StatusHistory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    """
    Serializer basique pour afficher info utilisateur dans les tickets
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class StatusHistorySerializer(serializers.ModelSerializer):
    """
    Serializer pour l'historique des changements de statut
    """
    changed_by = UserBasicSerializer(read_only=True)
    old_status_display = serializers.CharField(
        source='get_old_status_display', 
        read_only=True
    )
    new_status_display = serializers.CharField(
        source='get_new_status_display',
        read_only=True
    )
    
    class Meta:
        model = StatusHistory
        fields = [
            'id', 
            'old_status', 
            'new_status',
            'old_status_display',
            'new_status_display',
            'changed_by', 
            'changed_at'
        ]
        read_only_fields = ['id', 'changed_at']


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer principal pour les tickets
    """
    created_by = UserBasicSerializer(read_only=True)
    status_history = StatusHistorySerializer(many=True, read_only=True)
    attachment = serializers.FileField(required=False, allow_null=True)
    
    # Champs pour afficher les labels lisibles
    category_display = serializers.CharField(
        source='get_category_display',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    
    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'description',
            'category',
            'category_display',
            'status',
            'status_display',
            'attachment',
            'attachment_url',
            'created_by',
            'created_at',
            'updated_at',
            'status_history'
        ]
        read_only_fields = [
            'id',
            'created_by',
            'created_at',
            'updated_at',
            'attachment_url',
            'status'  # Le statut ne peut être modifié que via update_status
        ]
    
    def create(self, validated_data):
        """
        Créer un nouveau ticket avec l'utilisateur connecté
        """
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_attachment(self, value):
        """
        Valider la taille et le type du fichier
        """
        if value:
            # Vérifier la taille (max 10MB)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError(
                    "Le fichier ne doit pas dépasser 10MB"
                )
            
            # Vérifier le type de fichier
            allowed_types = [
                'image/jpeg', 'image/png', 'image/gif',
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            ]
            
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    "Type de fichier non autorisé. Utilisez: images, PDF, Word"
                )
        
        return value


class TicketCreateSerializer(serializers.ModelSerializer):
    """
    Serializer simplifié pour la création de tickets
    """
    attachment = serializers.FileField(required=False, allow_null=True)
    
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category', 'attachment']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class TicketStatusUpdateSerializer(serializers.Serializer):
    """
    Serializer pour mettre à jour uniquement le statut (Admin only)
    """
    status = serializers.ChoiceField(choices=Ticket.STATUS_CHOICES)
    
    def validate_status(self, value):
        """
        Validation personnalisée du statut
        """
        instance = self.instance
        
        # Ne pas permettre de revenir à 'new' depuis 'resolved'
        if instance and instance.status == 'resolved' and value == 'new':
            raise serializers.ValidationError(
                "Impossible de revenir au statut 'New' depuis 'Resolved'"
            )
        
        return value
    
    def update(self, instance, validated_data):
        """
        Mettre à jour le statut et créer l'historique
        """
        old_status = instance.status
        new_status = validated_data['status']
        
        # Seulement si le statut change
        if old_status != new_status:
            instance.status = new_status
            instance.save()
            
            # Créer l'entrée d'historique
            StatusHistory.objects.create(
                ticket=instance,
                old_status=old_status,
                new_status=new_status,
                changed_by=self.context['request'].user
            )
        
        return instance


class TicketListSerializer(serializers.ModelSerializer):
    """
    Serializer léger pour la liste des tickets (sans historique)
    """
    created_by = UserBasicSerializer(read_only=True)
    category_display = serializers.CharField(
        source='get_category_display',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    
    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'description',
            'category',
            'category_display',
            'status',
            'status_display',
            'attachment_url',
            'created_by',
            'created_at',
            'updated_at'
        ]