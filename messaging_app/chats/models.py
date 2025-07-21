from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
import uuid

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone_number, role, password=None, **extra_fields):
        if not all([first_name, last_name, email]):
            return ValueError("This field may not be blank!")
        email = self.normalize_email(email)
        user = self.model(first_name, last_name, email, phone_number, role, **extra_fields)
        user.set_pasword(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, phone_number, role="admin", password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            return ValueError("Superuser must have is_staff set to True")
        if not extra_fields.get("is_superuser"):
            return ValueError("Superuser must have is_superuser set to True")
        
        return self.create_user(first_name, last_name, email, phone_number, role, password, **extra_fields)

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(null=False, unique=True, db_index=True)
    phone_number = models.CharField(max_length=16, null=True)
    role = models.CharField(max_length=6, default="guest")
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE())
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now=True)

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    participants_id = models.ForeignKey(User, on_delete=models.CASCADE())
    created_at = models.DateTimeField(auto_now=True)

   
