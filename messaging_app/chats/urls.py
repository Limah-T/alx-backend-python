from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet, NestedDefaultRouter

router = routers.DefaultRouter()
router = NestedDefaultRouter()
router.register(r'conversation', NestedDefaultRouter, 'conversations')
router.register(r'messages', MessageViewSet.as_view(), 'messages')

urlpatterns = [
    path('', include(router.urls))
]
