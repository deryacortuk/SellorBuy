from phonenumber_field.formfields import PhoneNumberField
from django import forms
from .models import Profile, PhoneNumber
from django.utils.translation import gettext_lazy as _




class PhoneNumberForm(forms.ModelForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': _('Phone')}),  label=_("Phone number"), required=False)
    class Meta:
        model = PhoneNumber
        fields = ['phone_number']
 
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','bio','instagram_url']
    

    