from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, **kwargs):
    print(f"{instance} has been saved")
    receiver = instance.receiver
    Notification.objects.create(
        receiver=receiver,
        message=instance)
