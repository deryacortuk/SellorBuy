from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, PhoneNumber
from .forms import ProfileForm, PhoneNumberForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.http.response import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls.base import reverse,reverse_lazy
from django.contrib import  messages
from Product.models import Category

@login_required
def profile_user(request):
    data = Category.objects.all()
    profile = get_object_or_404(Profile, user = request.user)
    return render(request,"profile/profile.html",{"profile":profile, "data":data})

    
@login_required
def profileuser(request):
    data = Category.objects.all()
    profile = get_object_or_404(Profile,user = request.user)
    
    form = ProfileForm(instance = profile)
    
    if request.method =="POST":
        form = ProfileForm(request.POST, request.FILES, instance = request.user.profile)
        
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse('profile:user'))
        else:
            return render(request,'Profile/profile_edit.html',{'form':form,"data":data})
    return render(request,'Profile/profile_edit.html',{'form':form,"data":data})

class PasswordsChangeView(PasswordChangeView):
    form_class =PasswordChangeForm
    extra_context = {"data":Category.objects.all()}
    success_url = reverse_lazy('profile:passwordsuccess')

@login_required
def password_success(request):
    data = Category.objects.all()    
    return redirect("profile:user",data=data)
     
 

@login_required
def add_telephone(request):
    form = PhoneNumberForm()
    data = Category.objects.all()
    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone = form.save(commit=False)
            phone.user = request.user
            phone.save()
            return redirect("profile:user")
        else:
            return render(request,"profile/phone.html",{"form":form,"data":data})
    return render(request,"profile/phone.html",{"form":form,"data":data})
        
