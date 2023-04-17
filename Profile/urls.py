from django.urls import path
from . import views

app_name = "profile"

urlpatterns = [
    path("",views.profile_user, name="user"),
     path('edit/',views.profileuser,name='profile_update'),
        path('success/',views.password_success,name="passwordsuccess"),        
        path('phone/',views.add_telephone,name='telephone'),        
    path('changepassword/',views.PasswordsChangeView.as_view(template_name='profile/password.html'),name="passwordchange"),
]