from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("isCustomer:", getattr(request.user, 'isCustomer', None))
        return hasattr(request.user, 'isCustomer') and request.user.isCustomer
        

class IsCustomerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if hasattr(request.user, 'isCustomer') and request.user.isCustomer:
            customer_id = view.kwargs.get('customer_id')


            if str(customer_id) == str(request.user.id):
                return True

        return False