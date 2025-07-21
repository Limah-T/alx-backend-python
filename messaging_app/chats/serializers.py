from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(format="hex_verbose", read_only=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=16)
    created_at = serializers.DateTimeField()

    def create(self, validated_data):
        firstname = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        email = validated_data.get("email")
        if not all([firstname, last_name, email]):
            raise serializers.ValidationError("This field may not be blank")
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    message_id = serializers.UUIDField(format="hex_verbose", read_only=True)
    sender_id = serializers.UUIDField(format="hex_verbose", read_only=True)
    message_body = serializers.CharField(max_length=255)
    sent_at = serializers.DateTimeField()

    def create(self, validated_data):
        message_body = validated_data.get("message_body")
        if not message_body:
            raise serializers.ValidationError("This field may not be blank")
        return super().create(validated_data)

class ConversationSerializer(serializers.ModelSerializer):
    conversation_id = serializers.UUIDField(format="hex_verbose", read_only=True)
    participant_id = serializers.UUIDField(format="hex_verbose", read_only=True)
    created_at = serializers.DateTimeField()
    messages = serializers.SerializerMethodField()

    def get_messages(self, obj):
        ...



    