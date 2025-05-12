from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .permissions import IsCustomerOrAdmin
from ..auth import CustomerAuthentication
from rest_framework.response import Response 
from base.models import Customer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='get',
    operation_description="Returns customer account information",
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
@authentication_classes([CustomerAuthentication])
@permission_classes([IsCustomerOrAdmin])
def getCustomerAccount(request, customer_id=None):
    try:
        if customer_id:
            customer = Customer.objects.get(id=customer_id)
        else:
            customer = request.user
            
    except Customer.DoesNotExist:
        return Response({
            "error_status": status.HTTP_404_NOT_FOUND,
            "error_description": "Customer not found"
        }, status=status.HTTP_404_NOT_FOUND)

    customer_data = {
        "name": customer.name,
        "status": customer.status,
    }
    
    return Response(customer_data, status=status.HTTP_200_OK)

