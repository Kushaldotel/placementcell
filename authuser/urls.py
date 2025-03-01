from django.urls import path
from .views import UserLoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import GoogleAuthAPIView,  google_auth_callback

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path("google/", GoogleAuthAPIView.as_view(), name="google_auth"),
    # path("oauth_test/", google_auth_test_view, name="google-auth-test"),  # URL for template
    path("google/callback/", google_auth_callback, name="google_callback"),
]