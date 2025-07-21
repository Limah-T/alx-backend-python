from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["user_id", "first_name", "last_name", "email", "phone_number", "created_at"]

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ["message_id", "sender_id.first_name", "message_body", "sent_at"]

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer()

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participant_id", "created_at"]