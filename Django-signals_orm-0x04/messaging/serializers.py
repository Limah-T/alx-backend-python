from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth.hashers import make_password
from .models import User, Message, Notification, MessageHistory

class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=50, min_length=4)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    date_joined = serializers.DateTimeField(read_only=True)

    messages = serializers.SerializerMethodField()
    # notification = serializers.SerializerMethodField()

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError({'error': 'This field may not be blank'})
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError({'error': 'Username has been taken!'})
        return value.strip().lower()
    
    def validate(self, attrs):
        if len(attrs.get('password')) < 8 and len(attrs.get('password2')) < 8:
            raise serializers.ValidationError({'error': 'Minimum length of password should be 8'})
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({'error': 'Passwords do not match'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        username = validated_data.get('username')
        password = validated_data.get('password')
        hashed_password = make_password(password)
        # Create a user instance
        return User.objects.create(username=username, password=hashed_password)
    
    def get_messages(self, obj):
        return MessageSerializer(obj.inbox.all(), many=True).data
        
class MessageSerializer(serializers.Serializer):
    # Input
    receiver = serializers.CharField(write_only=True)

    # Output
    id = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all())
    sender = serializers.SlugRelatedField(slug_field='username',
                            queryset=User.objects.all(), 
                            required=False)
    content = serializers.CharField(max_length=255)
    
    receiver = serializers.SlugRelatedField(slug_field='username',queryset=User.objects.all(), required=False)
    timestamp = serializers.DateTimeField(read_only=True)

    def validate_recipient(self, value):
        if not value:
            raise serializers.ValidationError({'error': 'This field may not be blank'})
        if not User.objects.filter(username__iexact=value.strip()).exists():
            raise serializers.ValidationError({'error': 'Name does not exist'})
        return value.strip().lower()

    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError({'error': 'This field may not be blank'})
        return value.strip()
    
    def validate_sender(self, value):
        return value.username

    def validate_receiver(self, value):
        if value:
            val = value.username.strip().lower()
            if User.objects.filter(username__iexact=val).exists():
                raise serializers.ValidationError("You can't change the message owner to another user.")
            return value
    
class MessageHistorySerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=MessageHistory.objects.all())
    edited_by = serializers.CharField(read_only=True)
    old_content = serializers.CharField(read_only=True)
    recipient = serializers.CharField(read_only=True)
    edited_at = serializers.DateTimeField(read_only=True)



