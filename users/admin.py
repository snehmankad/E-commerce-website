from django.contrib import admin
from .models import Vendor, Customer, User
from .forms import VendorRegistrationForm, CustomerRegistrationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms

# Register your models here.
''' class UserAdmin(admin.ModelAdmin):
    model = User
    filter_horizontal = ('is_vendor', 'is_customer')

class CustomUserAdmin(UserAdmin):
        fieldsets = (
            *UserAdmin.fieldsets,
            (
                None,
                {
                    "fields": ('first_name', 'last_name'),
                },
            ),
        )

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name','is_vendor', 'is_customer')}
        ),
    )

# for vendor model:

class VendorCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Vendor
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class VendorAdmin(BaseUserAdmin):
    add_form = VendorCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name','email')}
        ),
    ) '''

class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'items_bought')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('is_vendor', ),}),)


admin.site.register(Vendor)
admin.site.register(Customer)
admin.site.register(User, UserAdmin)