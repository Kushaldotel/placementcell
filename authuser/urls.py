from django.urls import path
from .views import UserLoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
]