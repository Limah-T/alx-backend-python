# from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'api/conversation', ConversationViewSet.as_view(), 'conversations')
router.register(r'api/messages', MessageViewSet.as_view(), 'messages')
