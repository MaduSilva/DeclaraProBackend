import random
import string 
from rest_framework import serializers
from base.models import Customer, Document
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password 

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

    def create(self, validated_data):
        email = validated_data.get('email')
        
        if Customer.objects.filter(username=email).exists():
            raise serializers.ValidationError("Erro: Já existe um cliente com esse endereço de email cadastrado.")
        
        validated_data['username'] = email

        raw_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        validated_data['password'] = make_password(raw_password)

        customer = Customer.objects.create(**validated_data)
        customer.raw_password = raw_password
        return customer

class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        return value