from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from base.models import Customer
from django.conf import settings
import jwt

class CustomerAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            token = auth_header.split(' ')[1]

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            is_customer = payload.get('isCustomer', False) 

            customer = Customer.objects.get(id=user_id)

            customer.isCustomer = is_customer

        except (IndexError, jwt.ExpiredSignatureError, jwt.DecodeError) as e:
            raise AuthenticationFailed('Invalid or expired token.')
        except Customer.DoesNotExist:
            raise AuthenticationFailed('User not found.')

        return (customer, token)