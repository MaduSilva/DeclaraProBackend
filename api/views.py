from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from base.models import Customer
from .serializers import CustomerSerializer, DocumentSerializer

# Customer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCustomer(request, customer_id=None):
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
            serializer = CustomerSerializer(customer)
            customer_data = serializer.data
            if not customer_data.get('documents'):
                customer_data['documents'] = "Sem documentos cadastrados"
            return Response(customer_data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"detail": "Cliente não encontrado"}, status=status.HTTP_404_NOT_FOUND)
    else:
        items = Customer.objects.all()
        serializer = CustomerSerializer(items, many=True)
        customer_data = serializer.data
        for customer in customer_data:
            if not customer.get('documents'):
                customer['documents'] = "Sem documentos cadastrados"
        return Response(customer_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postCustomer(request):
    serializer = CustomerSerializer(data=request.data) 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)  
    return Response({
        "error_status": status.HTTP_400_BAD_REQUEST,  
        "error_description": "Dados inválidos."  
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteCustomer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Customer.DoesNotExist:
        return Response({
            "error_status": status.HTTP_404_NOT_FOUND,
            "error_description": "Cliente não encontrado."
        }, status=status.HTTP_404_NOT_FOUND)


# Document

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postDocument(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({"error": "Customer não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    serializer = DocumentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(customer=customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({
        "error_status": status.HTTP_400_BAD_REQUEST,  
        "error_description": "Dados inválidos."  
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteDocument(request, customer_id, document_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({
            "error_status": status.HTTP_404_NOT_FOUND,
            "error_description": "Cliente não encontrado."
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        document = customer.documents.get(id=document_id)
    except Document.DoesNotExist:
        return Response({
            "error_status": status.HTTP_404_NOT_FOUND,
            "error_description": "Documento não encontrado."
        }, status=status.HTTP_404_NOT_FOUND)

    document.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def renameDocument(request, customer_id, document_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({
            "error_status": status.HTTP_404_NOT_FOUND,
            "error_description": "Cliente não encontrado."
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        document = customer.documents.get(id=document_id)
    except Document.DoesNotExist:
        return Response({
            "error_status": status.HTTP_404_NOT_FOUND,
            "error_description": "Documento não encontrado."
        }, status=status.HTTP_404_NOT_FOUND)

    new_name = request.data.get('name')
    if not new_name:
        return Response({
            "error_status": status.HTTP_400_BAD_REQUEST,
            "error_description": "Nome do documento não fornecido."
        }, status=status.HTTP_400_BAD_REQUEST)

    document.name = new_name
    document.save()

    return Response({
        "message": "Documento renomeado com sucesso.",
        "document": DocumentSerializer(document).data
    }, status=status.HTTP_200_OK)