from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import random
import string

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    birthDate = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=110)
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)  
    password = models.CharField(max_length=255, blank=True, null=True)  
    
    def generate_username_and_password(self):
        self.username = self.email
        raw_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        self.password = make_password(raw_password)
        
       
        
        return raw_password

    def save(self, *args, **kwargs):
        if not self.username or not self.password:
            self.generate_username_and_password() 
        super(Customer, self).save(*args, **kwargs)
    
    @property
    def is_authenticated(self):
        return True

class Document(models.Model):
    customer = models.ForeignKey(Customer, related_name='documents', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if Document.objects.filter(customer=self.customer, name=self.name).exists():
            raise ValidationError(f"A document with the name '{self.name}' already exists for this customer.")

    def save(self, *args, **kwargs):
        self.clean()
        super(Document, self).save(*args, **kwargs)