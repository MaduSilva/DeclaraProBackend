from django.urls import path
from .views import getCustomer, postCustomer, postDocument, deleteCustomer, deleteDocument

urlpatterns = [
    path('customers/', getCustomer, name='customer-list'),
    path('customers/<int:customer_id>/', getCustomer, name='customer'),
    path('customers/add/', postCustomer, name='customer-add'),
    path('customers/remove/<int:customer_id>/', deleteCustomer, name='customer-delete'),
    path('customers/<int:customer_id>/documents/add/', postDocument, name='document-add'),
    path('customers/<int:customer_id>/documents/<int:document_id>/', deleteDocument, name='delete-document'),
]