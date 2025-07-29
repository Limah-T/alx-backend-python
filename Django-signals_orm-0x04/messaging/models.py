from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outbox')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox')
    content = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.content:
            self.content = self.content.strip()
        super().save(*args, **kwargs)   

class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name='notification') 
    timestamp = models.DateTimeField(auto_now_add=True)


