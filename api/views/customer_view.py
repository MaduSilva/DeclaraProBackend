from rest_framework.decorators import api_view, permission_classes
from .permissions import IsAdmin
from rest_framework.response import Response 
from base.models import Customer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.serializers import CustomerSerializer, PasswordResetSerializer
from django.contrib.auth.hashers import check_password, make_password
import re


@swagger_auto_schema(
    method='get',
    operation_description="Returns customer information. If a customer ID is provided, returns information for the specified customer; otherwise, returns information for all customers.",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Enter the token in format: 'Bearer' + token",
            type=openapi.TYPE_STRING,
            required=True
        )
    ]
)

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
            return Response({
            "error_status": status.HTTP_404_NOT_FOUND,
            "error_description": "Customer not found"
        }, status=status.HTTP_404_NOT_FOUND)
    else:
        items = Customer.objects.all()
        serializer = CustomerSerializer(items, many=True)
        customer_data = serializer.data
        return Response(customer_data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    operation_description="Add a new customer",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Enter the token in format: 'Bearer' + token",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Customer name'),
            'cpf': openapi.Schema(type=openapi.TYPE_STRING, description='Customer CPF'),
            'birthDate': openapi.Schema(type=openapi.TYPE_STRING, description='Customer birthDate. Must be in the format: "YYYY-MM-DD" (ex: "1999-01-01")'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Customer email'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Customer phone number in the format: "AreaCode + Number" (ex: "11999999999")'),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Customer IRPF declaration status'),
        },
        required=['name', 'cpf', 'birthDate', 'email', 'phone', 'status']
    ),
)

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
        "error_description": "The provided data is invalid"  
    }, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='delete',
    operation_description="Removes a customer by ID",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Enter the token in format: 'Bearer' + token",
            type=openapi.TYPE_STRING,
            required=True
        )
    ]
)

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
            "error_description": "Customer not found"
        }, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(
    method='patch',
    operation_description="Edit customer information by ID.",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Enter the token in format: 'Bearer' + token",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    )
)

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
            "error_description": "Customer not found."
        }, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='patch',    
    operation_description="Edit customer password by ID.",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Enter the token in format: 'Bearer' + token",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Customer new password'),
        },
    )
   
)

@api_view(['PATCH'])
@permission_classes([IsAdmin])
def resetPasswordCustomer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({
            "error_status": status.HTTP_404_NOT_FOUND,
            "error_description": "Customer not found"
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        new_password = serializer.validated_data['password']
        
        customer.password = make_password(new_password)
        customer.save()

        return Response({
            "description": "Password successfully reset"
        }, status=status.HTTP_200_OK)

    return Response({
        "error_status": status.HTTP_400_BAD_REQUEST,
        "error_description": "The provided data is invalid"
    }, status=status.HTTP_400_BAD_REQUEST)


def sanitize_cpf(cpf):
    if not cpf:
        return cpf
    
    clean_cpf = re.sub(r'\D', '', cpf)
    
    if len(clean_cpf) != 11:
        return cpf
    
    return f"{clean_cpf[:3]}.***.***-*{clean_cpf[-1]}"


@swagger_auto_schema(
    method='get',
    operation_description="Returns sanitized customer information for dashboard display. Returns customer name, masked CPF, and status for all customers.",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Enter the token in format: 'Bearer' + token",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Successful response",
            examples={
                "application/json": [
                    {
                        "Nome do Cliente": "João Silva",
                        "CPF": "407.***.***-*6",
                        "Status da Demanda": "Em Andamento"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
@permission_classes([IsAdmin])
def getSanitizedCustomers(request):
    customers = Customer.objects.all()
    
    sanitized_data = []
    for customer in customers:
        sanitized_customer = {
            "Nome do Cliente": customer.name,
            "CPF": sanitize_cpf(customer.cpf),
            "Status da Demanda": customer.status
        }
        sanitized_data.append(sanitized_customer)
    
    return Response(sanitized_data, status=status.HTTP_200_OK)