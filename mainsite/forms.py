from users.models import Customer
from mainsite.models import Item
from django import forms
from users.models import User

class BuyForm(forms.ModelForm):
    quantity_required = forms.IntegerField(initial=0)

    class Meta:
        model = Item
        fields = ('quantity_required',)

class AddMoneyForm(forms.ModelForm):
    money_owned = forms.DecimalField(min_value=0, label="Add Money")

    class Meta:
        model = User
        fields = ('money_owned',)