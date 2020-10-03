from django import forms
from .models import Vendor, Customer, User
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm


class VendorRegistrationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
   

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_vendor = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        vendor = Vendor.objects.create(user=user)
        vendor.username = self.cleaned_data.get('username')
        vendor.email = self.cleaned_data.get('email')
        vendor.save()
        return vendor

class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    add_fieldsets = (
        (
            None, {'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')}
        )
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
     

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.username = self.cleaned_data.get('username')
        customer.email = self.cleaned_data.get('email')
        customer.save()
        return customer


        