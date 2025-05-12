from rest_framework.decorators import api_view
from rest_framework.response import Response 
from base.models import Customer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

@swagger_auto_schema(
    method='post',
     operation_description="Login customer-account",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Customer username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Customer password'),
        },
        required=['username', 'password']
    ),
)

@api_view(['POST'])
def loginCustomerAccount(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({
            "error_status": status.HTTP_400_BAD_REQUEST,
            "error_description": "Username and password are required."
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        customer = Customer.objects.get(username=username)
    except Customer.DoesNotExist:
        return Response({
            "error_status": status.HTTP_401_UNAUTHORIZED,
            "error_description": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password, customer.password):
        return Response({
            "error_status": status.HTTP_401_UNAUTHORIZED,
            "error_description": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(customer)

    refresh['isCustomer'] = True 

    access_token = str(refresh.access_token)

    return Response({
        'refresh': str(refresh),
        'access': access_token
    }, status=status.HTTP_200_OK)

