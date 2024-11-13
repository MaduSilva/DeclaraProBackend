from django.contrib.auth.hashers import check_password, make_password
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from base.models import Customer
from .auth import CustomerAuthentication
from .serializers import CustomerSerializer, DocumentSerializer, PasswordResetSerializer

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
        
class IsCustomerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if hasattr(request.user, 'isCustomer') and request.user.isCustomer:
            customer_id = view.kwargs.get('customer_id')


            if str(customer_id) == str(request.user.id):
                return True

        return False


@api_view(['GET'])
@authentication_classes([CustomerAuthentication])
@permission_classes([IsCustomerOrAdmin])
def getCliente(request, customer_id=None):
    try:
        if customer_id:
            customer = Customer.objects.get(id=customer_id)
        else:
            customer = request.user
            
    except Customer.DoesNotExist:
        return Response({"detail": "Cliente não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    customer_data = {
        "name": customer.name,
        "status": customer.status,
    }
    
    return Response(customer_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdmin])
def getCustomer(request, customer_id=None):
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
            serializer = CustomerSerializer(customer)
            customer_data = serializer.data
            return Response(customer_data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"detail": "Cliente não encontrado"}, status=status.HTTP_404_NOT_FOUND)
    else:
        items = Customer.objects.all()
        serializer = CustomerSerializer(items, many=True)
        customer_data = serializer.data
        return Response(customer_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAdmin])
def postCustomer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.save()

        response_data = serializer.data
        response_data['raw_password'] = customer.raw_password

        return Response(response_data, status=status.HTTP_201_CREATED)

    return Response({
        "error_status": status.HTTP_400_BAD_REQUEST,  
        "error_description": "Dados inválidos."  
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdmin])
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

@api_view(['PATCH'])
@permission_classes([IsAdmin])
def editCustomer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)

        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Customer.DoesNotExist:
        return Response({
            "error_status": status.HTTP_404_NOT_FOUND,
            "error_description": "Customer não encontrado."
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAdmin])
def resetPasswordCustomer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({
            "error_status": status.HTTP_404_NOT_FOUND,
            "error_description": "Cliente não encontrado."
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        new_password = serializer.validated_data['password']
        
        customer.password = make_password(new_password)
        customer.save()

        return Response({
            "message": "Senha redefinida com sucesso."
        }, status=status.HTTP_200_OK)

    return Response({
        "error_status": status.HTTP_400_BAD_REQUEST,
        "error_description": "Dados inválidos."
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def loginCustomer(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        customer = Customer.objects.get(username=username)
    except Customer.DoesNotExist:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password, customer.password):
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(customer)

    refresh['isCustomer'] = True 

    access_token = str(refresh.access_token)

    return Response({
        'refresh': str(refresh),
        'access': access_token
    }, status=status.HTTP_200_OK)


# Document

@api_view(['POST'])
@permission_classes([IsAdmin])
def postDocument(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({
        "error_status": status.HTTP_404_NOT_FOUND,  
        "error_description": "Customer não encontrado."  
    }, status=status.HTTP_404_NOT_FOUND)

    serializer = DocumentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(customer=customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({
        "error_status": status.HTTP_400_BAD_REQUEST,  
        "error_description": "Dados inválidos."  
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdmin])
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
@permission_classes([IsAdmin])
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