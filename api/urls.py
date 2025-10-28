from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views.customer_view import getCustomer, postCustomer, deleteCustomer, editCustomer, resetPasswordCustomer, getSanitizedCustomers
from .views.document_view import postDocument, deleteDocument, renameDocument
from .views.auth_view import loginCustomerAccount
from .views.customer_account_view import getCustomerAccount
from .views.calculator_view import calculateIRPF

schema_view = get_schema_view(
    openapi.Info(
        title="Customer API",
        default_version="v1",
        description="API documentation for Customer management",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
    path('customers/', getCustomer, name='customer-list'),
    path('customers/dashboard/', getSanitizedCustomers, name='customer-sanitized-list'),
    path('customers/<int:customer_id>/', getCustomer, name='customer'),
    path('customers/add/', postCustomer, name='customer-add'),
    path('customers/remove/<int:customer_id>/', deleteCustomer, name='customer-delete'),
    path('customers/edit/<int:customer_id>/', editCustomer, name='customer-edit'),
    path('customers/reset-password/<int:customer_id>/', resetPasswordCustomer, name='customer-reset-password'),
    path('customers/<int:customer_id>/documents/', postDocument, name='document-add'),
    path('customers/<int:customer_id>/documents/<int:document_id>/', deleteDocument, name='delete-document'),
    path('customers/<int:customer_id>/documents/<int:document_id>/rename/', renameDocument, name='rename-document'),


    # customer-account
    path('customer-account/login', loginCustomerAccount, name='customer-account-login'),
    path('customer-account/<int:customer_id>/info', getCustomerAccount, name='get-customer-account'),
    path('customer-account/calculator', calculateIRPF, name='calculate-irpf'),

    # Swagger URLs
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
