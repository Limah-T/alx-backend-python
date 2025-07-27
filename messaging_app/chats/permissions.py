from rest_framework.permissions import BasePermission
from .models import Conversation

class IsParticipantOfConversation(BasePermission):

    def has_permission(self, request, view):
        active_user = request.user.is_active
        authenticated_user = request.user.is_authenticated
        return active_user and authenticated_user

    def has_object_permission(self, request, view, obj):
        user_id = request.user.id
        if Conversation.objects.filter(participants=user_id).exists():
            return True
        
