from django.test import TestCase
from django.contrib.auth.hashers import make_password
from dj_rest_auth.views import LoginView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.contrib.auth import login
from .models import User, Message, Conversation
from .serializers import RegisterSerializer, CustomLoginSerializer, MessageSerializer, ConversationSerializer
from datetime import datetime

class RegisterViewset(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')
        password = make_password(password)
        User.objects.create(
                        username=serializer.validated_data.get("username"),
                        first_name=serializer.validated_data.get("first_name"),
                        last_name=serializer.validated_data.get("last_name"),
                        email=serializer.validated_data.get("email"),
                        phone_number=serializer.validated_data.get("phone_number"),
                        password=password)
        return Response("Account created successfully", status=status.HTTP_200_OK)


class CustomLoginView(LoginView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CustomLoginSerializer

    # def dispatch(self, request, *args, **kwargs):
    #     for token in OutstandingToken.objects.filter(user=request.user):
    #         try:
    #             BlacklistedToken.objects.get(token=token)
    #         except BlacklistedToken.DoesNotExist:
    #             BlacklistedToken.objects.create(token=token)
    #     return super().dispatch(request, *args, **kwargs)

    def get_response(self):
        response_data = super().get_response()
        # Removes user data and return only access and refresh token
        response_data.data.pop("user")
        
        return Response(data=response_data.data)
    
class ALLUserViewset(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    queryset = User.objects.all()     
    
    def list(self, request):
        serializer = RegisterSerializer(self.queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class ConversationViewSet(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all()

    def list(self, request):
        data = Conversation.objects.filter(participants_id=request.user)
        serializer = ConversationSerializer(data, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
        
# ["filters"]
class MessageViewSet(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def list(self, request):
        data = Message.objects.filter(sender_id=request.user)
        serializer = MessageSerializer(data=data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data.get("message_body")
        message_instance = Message.objects.create(sender=request.user, message_body=message, sent_at=datetime.today())
        Conversation.objects.create(message=message_instance, participants=request.user, created_at=datetime.today())
        return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
    
