from django import forms
from Order.models import Order
from django_countries.widgets import CountrySelectWidget


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        widgets = {"country": CountrySelectWidget()}
        fields = ["email","phone_number",'country',"city","state","district","address","appartment","zip_code","comment"]
        
        
        