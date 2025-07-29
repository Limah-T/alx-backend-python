from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.jwt_auth import JWTAuthentication
from dj_rest_auth.views import LoginView
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, MessageSerializer
from .models import User, Message

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
    http_method_names = ["post", "get"]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.select_related('sender', 'receiver').all()
    
    def create(self, request, *args, **kwargs):
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
    
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({'success':'Successfully retrieved all messages',
                        'data':serializer.data}, status=status.HTTP_200_OK)
   
'''
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUzODEzODY4LCJpYXQiOjE3NTM4MTAyNjgsImp0aSI6ImZjY2U3MDM5MTk0MzRlY2ZiNjQ4YWQyYjM2ZmYwZDI1IiwidXNlcl9pZCI6IjQifQ.z-BHvTq3s6ed8X9vnDirIEV8KY5yZtkfA6r2fszhzHo",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1Mzg5NjY2OCwiaWF0IjoxNzUzODEwMjY4LCJqdGkiOiJiYWY5ZmUxNWFkZWQ0MWM3YTY0OTEyNWEyNzA4MTE1NyIsInVzZXJfaWQiOiI0In0.NixZ4_2BaXwWtxlIMcNBn8Mx8UMBooe7a6kiNUc5fEQ"
}
'''