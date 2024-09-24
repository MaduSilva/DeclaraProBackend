from django.urls import path
from .views import getCustomer, postCustomer, postDocument, deleteCustomer

urlpatterns = [
    path('customers/', getCustomer, name='customer-list'),
    path('customers/add/', postCustomer, name='customer-add'),
    path('customers/<int:customer_id>/', deleteCustomer, name='customer-delete'),
    path('customers/<int:customer_id>/documents/add/', postDocument, name='document-add'),
]