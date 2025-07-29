from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterViewSet, MessageModelViewSet, LoginViewset, UserViewSet

app_name = 'messaging'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterViewSet.as_view(), name='register'),
    path('login/', LoginViewset.as_view(), name='login'),
    path('users/', UserViewSet.as_view({'get': 'list'}), name='users'),
    path('messages/', MessageModelViewSet.as_view({'post': 'create', 'get': 'list'}), name='messages')
]