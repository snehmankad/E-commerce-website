from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_vendor=models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    items_bought = models.JSONField(default=list)
    money_owned = models.DecimalField(decimal_places=2, max_digits=10, default=0)

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        permissions = [('can_access_vendor_home', 'can access vendor home'),]

    def __str__(self):
        return self.username

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    
    class Meta:
        permissions = [('can_access_customer_home', 'can access customer home'),]

    def __str__(self):
        return self.username
