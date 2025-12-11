from rest_framework import serializers
from .models import Ticket, StatusHistory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class StatusHistorySerializer(serializers.ModelSerializer):
    changed_by = UserBasicSerializer(read_only=True)
    old_status_display = serializers.CharField(source='get_old_status_display', read_only=True)
    new_status_display = serializers.CharField(source='get_new_status_display', read_only=True)

    class Meta:
        model = StatusHistory
        fields = [
            'id', 'old_status', 'new_status',
            'old_status_display', 'new_status_display',
            'changed_by', 'changed_at'
        ]
        read_only_fields = ['id', 'changed_at']


class TicketSerializer(serializers.ModelSerializer):
    created_by = UserBasicSerializer(read_only=True)
    status_history = StatusHistorySerializer(many=True, read_only=True)
    attachment = serializers.FileField(required=False, allow_null=True)

    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description',
            'category', 'category_display',
            'status', 'status_display',
            'attachment', 'attachment_url',
            'created_by', 'created_at',
            'updated_at', 'status_history'
        ]
        read_only_fields = [
            'id', 'created_by', 'created_at',
            'updated_at', 'attachment_url', 'status'
        ]

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class TicketCreateSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category', 'attachment']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class TicketStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Ticket.STATUS_CHOICES)

    def validate_status(self, value):
        instance = self.instance
        if instance and instance.status == 'resolved' and value == 'new':
            raise serializers.ValidationError("Impossible de revenir au statut 'New' depuis 'Resolved'")
        return value

    def update(self, instance, validated_data):
        old_status = instance.status
        new_status = validated_data['status']

        if old_status != new_status:
            instance.status = new_status
            instance.save()
            StatusHistory.objects.create(
                ticket=instance,
                old_status=old_status,
                new_status=new_status,
                changed_by=self.context['request'].user
            )
        return instance


class TicketListSerializer(serializers.ModelSerializer):
    created_by = UserBasicSerializer(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description',
            'category', 'category_display',
            'status', 'status_display',
            'attachment_url', 'created_by',
            'created_at', 'updated_at'
        ]
