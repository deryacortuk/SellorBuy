from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    READ = "r"
    UNREAD ="u"
    
    CHOICES = ((READ, "read"), (UNREAD, "unread"))
    user = models.ForeignKey(User, related_name="notifications",on_delete=models.CASCADE)
    
    title = models.CharField(max_length=250, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    status = models.CharField(choices=CHOICES,default=UNREAD, max_length=1)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username


