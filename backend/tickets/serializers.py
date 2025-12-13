from rest_framework import serializers
from .models import Ticket
from accounts.serializers import UserSerializer

class TicketSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Ticket
        fields = ('id', 'title', 'description', 'status', 'created_by', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)