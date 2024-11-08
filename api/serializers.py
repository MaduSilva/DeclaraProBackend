from rest_framework import serializers
from base.models import Customer, Document
from django.core.exceptions import ValidationError


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name', 'file', 'uploaded_at']
    
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except ValidationError as e:
            raise serializers.ValidationError({"error": str(e)})

class CustomerSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'cpf', 'birthDate', 'email', 'phone', 'status', 'documents']