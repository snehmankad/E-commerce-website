from django.db import models
from users.models import User
from django.shortcuts import reverse

# Create your models here.
def f():
    return User.objects.first()

class Item(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, default=f)
    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    price = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    quantity_available = models.PositiveIntegerField(default=0)
    sales = models.IntegerField(default=0)
    quantity_required = models.PositiveIntegerField(default=0)
    image = models.ImageField(default='default.jpg', upload_to='item_pics')


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'pk':self.pk})
