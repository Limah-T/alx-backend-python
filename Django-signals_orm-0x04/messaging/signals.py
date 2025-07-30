from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Message, Notification, MessageHistory
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Message)
def create_notification(sender, instance, **kwargs):
    receiver = instance.receiver
    Notification.objects.create(
        receiver=receiver,
        message=instance)
    logger.info(f"{instance} has been created")
    logger.info(f"Notification sent to: {instance.receiver} at {instance.timestamp}")

@receiver(pre_save, sender=Message)
def create_message_history(sender, instance, **kwargs):
    try:
        old_content = Message.objects.get(id=instance.id)
    except Message.DoesNotExist:
        return 
    if instance.edited:
        mh=MessageHistory.objects.create(
            modifier=instance.sender,
            old_content=old_content.content,
            recipient=instance.receiver,
        )
        instance.edited=False
        logger.info(f"User: {instance.sender} => edited a message[{old_content.content}] to [{instance.content}] | Sent to {instance.receiver} at {mh.date_modified}")
