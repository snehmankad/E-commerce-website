"""my_ecommerce_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainsite.views import *
from users.views import *
from django.contrib.auth.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', customer_home, name='customer_home'),
    path('vendor_registration/', vendor_registration.as_view(), name='vendor_registration'),
    path('customer_registration/', customer_registration.as_view(), name='customer_registration'),
    path('login/', login_view, name='login'),
    path('vendor_home/', vendor_home, name='vendor_home'),
    path('logout/', logout_view, name='logout'),
    path('create_item/', ItemCreateView.as_view(), name='create_item'),
    path('item_detail/<int:pk>', ItemDetailView.as_view(), name='item_detail'),
    path('item_update/<int:pk>', ItemUpdateView.as_view(), name='item_update'),
    path('item_delete/<int:pk>', ItemDeleteView.as_view(), name='item_delete'),
    path('buy_item/<int:pk>', buy_item, name='buy_item'),
    path('buy_item_success/<int:pk>', buy_item_success, name='buy_item_success'),
    path('customer_items_bought/', customer_items_bought, name='customer_items_bought'),
    path('wallet/', wallet, name='wallet'),
    path('add_money', add_money, name='add_money'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
