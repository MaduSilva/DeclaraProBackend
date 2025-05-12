from rest_framework.decorators import parser_classes, api_view, permission_classes
from .permissions import IsAdmin
from rest_framework.response import Response 
from base.models import Customer, Document
from rest_framework import status
from api.serializers import DocumentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser
from django.core.exceptions import ValidationError


@swagger_auto_schema(
    method='post',
    operation_description="Add a new document to a customer",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Enter the token in format: 'Bearer' + token",
            type=openapi.TYPE_STRING,
            required=True
        ),
         openapi.Parameter(
            'name',
            openapi.IN_FORM,
            description="Document name",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'document_type',
            openapi.IN_FORM,
            description="Document type",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'file',
            openapi.IN_FORM,
            description="Document file",
            type=openapi.TYPE_FILE,
        ),
    ]
)

@api_view(['POST'])
@permission_classes([IsAdmin])
@parser_classes([MultiPartParser])
def postDocument(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({
        "error_status": status.HTTP_404_NOT_FOUND,  
        "error_description": "Customer not found"  
    }, status=status.HTTP_404_NOT_FOUND)

    serializer = DocumentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(customer=customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({
        "error_status": status.HTTP_400_BAD_REQUEST,  
        "error_description": "The provided data is invalid"  
    }, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='delete',
    operation_description="Delete a customers document by ID",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Enter the token in format: 'Bearer' + token",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ]
)

@api_view(['DELETE'])
@permission_classes([IsAdmin])
def deleteDocument(request, customer_id, document_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({
            "error_status": status.HTTP_404_NOT_FOUND,
            "error_description": "Customer not found."
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        document = customer.documents.get(id=document_id)
    except Document.DoesNotExist:
        return Response({
            "error_status": status.HTTP_404_NOT_FOUND,
            "error_description": "Document not found."
        }, status=status.HTTP_404_NOT_FOUND)

    document.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method='put',
    operation_description="Rename a document",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Enter the token in format: 'Bearer' + token",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Document new name'),
        },
        required=['name']
    )
)

@api_view(['PUT'])
@permission_classes([IsAdmin])
def renameDocument(request, customer_id, document_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({
            "error_status": status.HTTP_404_NOT_FOUND,
            "error_description": "Customer not found"
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        document = customer.documents.get(id=document_id)
    except Document.DoesNotExist:
        return Response({
            "error_status": status.HTTP_404_NOT_FOUND,
            "error_description": "Document not found"
        }, status=status.HTTP_404_NOT_FOUND)

    new_name = request.data.get('name')
    if not new_name:
        return Response({
            "error_status": status.HTTP_400_BAD_REQUEST,
            "error_description": "Invalid data"
        }, status=status.HTTP_400_BAD_REQUEST)

    document.name = new_name

    try:
        document.save()
    except ValidationError as e:
        return Response({
            "error_status": status.HTTP_400_BAD_REQUEST,
            "error_description": e.messages[0]
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            "error_status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "error_description": "An error ocourred while renaming the document. Try again later."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    return Response({
        "description": "Document renamed successfully",
        "document": DocumentSerializer(document).data
    }, status=status.HTTP_200_OK)