# from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversation', ConversationViewSet.as_view(), 'conversations')
router.register(r'messages', MessageViewSet.as_view(), 'messages')
