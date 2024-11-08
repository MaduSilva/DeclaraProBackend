from django.db import models
from django.core.exceptions import ValidationError

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    birthDate = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=110)

    def save(self, *args, **kwargs):
        if self.id is None and Customer.objects.filter(cpf=self.cpf).exists():
            pass
        else:
            super(Customer, self).save(*args, **kwargs)

class Document(models.Model):
    customer = models.ForeignKey(Customer, related_name='documents', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if Document.objects.filter(customer=self.customer, name=self.name).exists():
            raise ValidationError(f"Já existe um documento com o nome '{self.name}' para este cliente.")

    def save(self, *args, **kwargs):
        self.clean()
        super(Document, self).save(*args, **kwargs)