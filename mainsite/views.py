from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mainsite.models import Item
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from .forms import AddMoneyForm, BuyForm
from django.urls import reverse
from my_ecommerce_app.decorators import customer_permissions, vendor_permissions
from my_ecommerce_app.mixins import CustomerRequiredMixin, VendorRequiredMixin
from django.core.paginator import Paginator
from users.models import User

# to redirect vendor to this page after login
@login_required
def vendor_home(request):
    # shows items registered by vendor if he/she is logged in.
    user = request.user

    vendor_name = request.GET.get('name')
    try:
        user_common = User.objects.get(username=vendor_name)
    except:
        user_common = request.user
    
    items = Item.objects.filter(vendor=user_common).order_by('-sales')

    return render(request, 'mainsite/vendor_home.html', {'items':items, 'user_common':user_common})
    

# the default homepage for the site
def customer_home(request):
    user = request.user
    items = Item.objects.all().order_by('-sales')
    
    paginator = Paginator(items, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = True

    return render(request, 'mainsite/customer_home.html', {'items': items, 'page_obj':page_obj, 'is_paginated':is_paginated})
    
# to create new posts for vendors
class ItemCreateView(LoginRequiredMixin, VendorRequiredMixin, CreateView):
    model = Item
    template_name='mainsite/create_item.html'
    fields = ['title', 'description', 'price', 'quantity_available']

    def form_valid(self, form):
        form.instance.vendor = self.request.user
        return super().form_valid(form)

# a detail page for a particular item.
class ItemDetailView(DetailView):
    model = Item
    template_name = 'mainsite/item_detail.html' 

# a update form for every item
class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, VendorRequiredMixin, UpdateView):
    model = Item
    fields = ['title', 'description', 'price', 'quantity_available', 'image']
    template_name = 'mainsite/item_update.html'
    
    def form_valid(self, form):
        form.instance.vendor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.vendor:
            return True
        return False

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, VendorRequiredMixin, DeleteView):
    model = Item
    template_name = 'mainsite/item_delete.html'
    success_url = '/'

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.vendor:
            return True
        return False

@login_required
@customer_permissions
def buy_item(request, pk):  
    user = request.user 
    item_vendor = Item.objects.get(id=pk).vendor

    for i in user.items_bought:
        previous_vendor = Item.objects.get(id=i).vendor
        if (item_vendor != previous_vendor):
            messages.error(request, f'You are not allowed to buy items from different vendors.')
            return redirect('customer_home')
        elif i is not pk:
            messages.error(request, f'You are not allowed to buy different products from same vendor.' )
            return redirect('customer_home')

    if request.method=='POST':
        form = BuyForm(request.POST)
        if form.is_valid():
            item_new_info = form.save(commit=False) # if we do form.save() directly, the view creates a new instance of item every time it is called.
            quantity_bought = item_new_info.quantity_required 
            item = Item.objects.get(id=pk)
            if quantity_bought > 0 and item.quantity_available > 0 and quantity_bought <= item.quantity_available and user.money_owned >= item.price*quantity_bought:
                item.sales+=quantity_bought
                item.quantity_available-=quantity_bought
                user.money_owned-=item.price*quantity_bought
                item.save()
                user.save()          
            elif item.quantity_available < 1:
                messages.error(request, f'Item is Sold out :(')
                return redirect('/')
            elif quantity_bought > item.quantity_available:
                messages.error(request, f'Quantity selected should be less than {item.quantity_available}')
                return redirect('/')
            elif user.money_owned < item.price*quantity_bought:
                messages.error(request, f"You don't have sufficient amount in your wallet.")
                return redirect('wallet')
            elif quantity_bought == 0:
                messages.error(request, f"Select quantity.")
                return redirect(reverse('buy_item', kwargs={'pk':pk}))       
            
            return redirect(reverse('buy_item_success', kwargs={'pk':pk}))

        else:
            messages.error(request, "Form isn't valid. Try again")
            return redirect('/')

    else:
       form = BuyForm()

    return render(request, 'mainsite/buy_item.html', {'form': form})

@login_required
@customer_permissions
def buy_item_success(request, pk):
    customer = request.user
    if not (pk in customer.items_bought): # updates a list that contains all item ids bought by the customer
        customer.items_bought.append(pk)
        customer.save()

    return render(request, 'mainsite/buy_item_success.html')

@login_required
@customer_permissions
def customer_items_bought(request):
    user = request.user
    items = []

    for i in user.items_bought:
        items.append(Item.objects.get(id=i))

    paginator = Paginator(items, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = True

    return render(request, 'mainsite/customer_items_bought.html', {'items':items, 'page_obj':page_obj, 'is_paginated':is_paginated})

@login_required
@customer_permissions
def wallet(request):
    customer = request.user
    return render(request, 'mainsite/wallet.html', {'customer':customer})

@login_required
@customer_permissions
def add_money(request):
    if request.method=='POST':
        form = AddMoneyForm(data=request.POST)
        user = request.user
        if form.is_valid():
            user_new_info = form.save(commit=False) # to prevent new instance creation of user every time view is called.
            if user_new_info.money_owned == 0:
                messages.success(request, f"You haven't added any money to your wallet.")
                return redirect('wallet')
            else:
                user.money_owned += user_new_info.money_owned
                messages.success(request, f'You have successfully added {user_new_info.money_owned} rupees to your wallet')  
                user.save()        
                return redirect('wallet')
            

        else:
            messages.error(request, "form ain't valid.")
            return redirect('wallet')

    else:

        form = AddMoneyForm()

    return render(request, 'mainsite/add_money.html', {'form': form})


