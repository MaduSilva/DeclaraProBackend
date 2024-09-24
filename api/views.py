from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status
from base.models import Customer
from .serializers import CustomerSerializer, DocumentSerializer

# Customer

@api_view(['GET'])
def getCustomer(request):
    items = Customer.objects.all()
    serializer = CustomerSerializer(items, many=True)

    for customer in serializer.data:
        if not customer['documents']:
            customer['documents'] = "Sem documentos cadastrados"

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
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
def deleteCustomer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  # Retorna 204 No Content quando a exclusão for bem-sucedida
    except Customer.DoesNotExist:
        return Response({
            "error_status": status.HTTP_404_NOT_FOUND,
            "error_description": "Cliente não encontrado."
        }, status=status.HTTP_404_NOT_FOUND)


# Document

@api_view(['POST'])
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