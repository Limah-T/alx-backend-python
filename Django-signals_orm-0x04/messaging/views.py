from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from dj_rest_auth.jwt_auth import JWTAuthentication
from dj_rest_auth.views import LoginView
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, MessageSerializer, MessageHistorySerializer
from .models import User, Message, MessageHistory

class RegisterViewSet(views.APIView):
    authentication_classes = []
    permission_classes = []
    http_method_names = ["post"]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class LoginViewset(LoginView):
    authentication_classes = []
    permission_classes = []
    http_method_names = ["post"]

    def get_response(self):
        response_data = super().get_response()
        # Removes user data and return only access and refresh token
        response_data.data.pop("user")
        
        return Response(data=response_data.data)
    
class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post", "get"]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class MessageModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post", "get", "patch", "put", "delete"]
    serializer_class = MessageSerializer
    pagination_class = [PageNumberPagination]

    def get_queryset(self):
        print("In here")
        return Message.objects.select_related('sender', 'receiver').all()
    
    def create(self, request, *args, **kwargs):
        print("In create")
        current_user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reciever = serializer.validated_data.get("recipient")
        content = serializer.validated_data.get("content")
        recipient = get_object_or_404(User, username=reciever)
        Message.objects.create(
            sender=current_user, receiver=recipient, 
            content=content)
        return Response({"success": f"Successfully sent message to {reciever}"},
                         status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({'success':'Successfully retrieved all messages',
                        'data':serializer.data}, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        id_exist = get_object_or_404(Message, id=kwargs.get('pk'))
        serializer = self.get_serializer(id_exist)
        print(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
       
    def update(self, request, *args, **kwargs):
        message = get_object_or_404(Message, id=kwargs.get('pk'))
        serializer = self.get_serializer(data=request.data, instance=message, partial=True)
        serializer.is_valid(raise_exception=True)
        message.receiver=message.receiver
        message.content=serializer.validated_data.get('content')
        message.edited=True
        message.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
    
class MessageHistoryModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    http_method_names = ["get"]
    serializer_class = MessageHistorySerializer
    queryset = MessageHistory.objects.all()

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(http_method_names=["delete"])
def delete_user(request):
    request.user.delete()
    return Response({'success': 'Account deleted successfully'}, status=status.HTTP_200_OK)


   
