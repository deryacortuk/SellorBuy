from django import forms 
from Profile.models import BankInformation

class BankCardForm(forms.ModelForm):
    class Meta:
        model = BankInformation
        fields = ["cardnumber"]