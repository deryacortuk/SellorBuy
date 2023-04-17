from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os
from phonenumber_field.modelfields import PhoneNumberField
# from Product.models import Products
import logging
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.crypto import get_random_string
import datetime
# from twilio.rest import Client
# from twilio.base.exceptions import TwilioRestExcption

from .images_handle import image_resize




logger = logging.getLogger(__name__)

class PhoneNumber(models.Model):
    user = models.OneToOneField(User, related_name="phone",on_delete=models.CASCADE)
    phone_number = PhoneNumberField(unique = True, null=True)
    security_code = models.CharField(max_length=120)
    is_verified = models.BooleanField(default=False)
    sent = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created_at',)
        
    def __str__(self):
        return self.phone_number.as_e164
    
    def generate_security_code(self):
        token_length = getattr(settings, "TOKEN_LENGTH",6)
        return get_random_string(token_length, allowed_chars = "0123456789")
    
    def is_security_code_experied(self):
        expiration_date = self.sent + datetime.timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
        return expiration_date <= timezone.now()
    
    # def send_confirmation(self):
    #     twilio_account_sid = settings.TWILIO_ACCOUNT_SID
    #     twilio_auth_token = settings.TWILIO_AUTH_TOKEN
    #     twilio_phone_number = settings.TWILIO_PHONE_NUMBER
        
    #     self.security_code = self.generate_security_code()
        
    #     if all([twilio_account_sid, twilio_auth_token,twilio_phone_number]):
    #         try:
    #             twilio_client = Client(twilio_account_sid, twilio_auth_token)
    #             twilio_client.messages.create(
    #                 body=f'Your activation code is {self.security_code}',
    #                 to=str(self.phone_number),
    #                 from=twilio_phone_number
    #             )
    #             self.sent = timezone.now()
    #             self.save()
    #             return True
    #         except TwilioRestException as e:
    #             print(e)
    #     else:
    #         print("Twilio credentials are not set")
    
    def check_verification(self,security_code):
        if (not self.is_security_code_experied() and security_code == self.security_code and self.is_verified == False):
            self.is_verified = True
            self.save()
        else:
            raise ValueError(_("Your security code is wrong, expired or this phone is verified before"))
        return self.is_verified
    

    
  

def user_profile_pic(instance, filename):
    user_pic_name = 'user_{0}/profile.png'.format(instance.user.id)
    return user_pic_name

class BankInformation(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="user_bank")
    cardnumber = models.CharField(max_length=30, null=True,blank=True)
    
    def __str__(self):
        return self.user.get_full_name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image =models.ImageField(upload_to=user_profile_pic, blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering = ('-created_at',)
        
    def __str__(self) -> str:
        return self.user.get_full_name()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img_path = self.image.path
            print(str(img_path))
            img = image_resize(img_path, 200) 
            new_img_path = img_path.split('.')[0]+'.jpg'
            os.remove(img_path)
            img.save(new_img_path, format='JPEG', quality=100, optimize=True)
            self.image = new_img_path
            super().save(*args, **kwargs)
        elif self.image == None:
            pass
    
  
        
        
 

    
    
    
    
    
    
    
