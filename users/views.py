from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm, VendorRegistrationForm
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from my_ecommerce_app.decorators import vendor_permissions, customer_permissions, login_not_allowed
from my_ecommerce_app.mixins import CustomerRequiredMixin, VendorRequiredMixin, LoginNotAllowedMixin

# Create your views here.

class vendor_registration(LoginNotAllowedMixin, CreateView):
    model = User
    form_class = VendorRegistrationForm
    template_name = 'users/vendor_registration.html'

    def form_valid(self, form):
        user = form.save()
        return redirect('/login/')
    
class customer_registration(LoginNotAllowedMixin, CreateView):
    model = User
    form_class = CustomerRegistrationForm
    template_name = 'users/customer_registration.html'

    def form_valid(self, form):
        user = form.save()
        return redirect('/login/')

@login_not_allowed
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_vendor == True:
                    return redirect('vendor_home')
                else:
                    return redirect('customer_home')
            else:
                messages.error(request, 'Invalid username or password. Please try again')
        else:
            messages.error(request, 'Invalid username or password. Please try again')
            
    return render(request, "users/login.html", {'form': AuthenticationForm()})

@login_required
def logout_view(request):
    messages.error(request, f'You have successfully logged out.')
    logout(request)
    return redirect('/')