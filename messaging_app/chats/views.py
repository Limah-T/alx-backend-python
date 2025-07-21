from django.test import TestCase
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer
from collections import namedtuple
from rest_framework.routers import SimpleRouter, Route

class NestedDefaultRouter(SimpleRouter):
    routes = [
       Route(
           url=r'^{prefix}/{lookup}$',
           mapping={'get': 'retrieve'},
           name='{basename}-detail',
           detail=True,
           initkwargs={'suffix': 'Detail'}
       ),

       Route(
           url=r'^{prefix}$',
           mapping={'get': 'list'},
           name='{basename}-list',
           detail=False,
           initkwargs={'suffix': 'List'}
       ) 
    ]


class ConversationViewSet(ViewSet):
    authentication_classes = []
    permission_classes = []

    @action(detail=True, methods=["GET"])
    def list(self, request):
        data = Conversation.objects.filter(participants_id=request.user)
        serializer = ConversationSerializer(data=data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def create(self, request):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
        
["filters"]
class MessageViewSet(ViewSet):
    authentication_classes = []
    permission_classes = []

    @action(detail=True, methods=["GET"])
    def list(self, request):
        data = Message.objects.filter(sender_id=request.user)
        serializer = MessageSerializer(data=data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["POST"])
    def create(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
    
