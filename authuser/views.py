from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserLoginSerializer
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from vacancy.permissions import IsStudentUser
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            # Get the user from the serializer
            user = serializer.validated_data.get('user')

            # Check if the user is of type 'STUDENT'
            if user.user_type != 'STUDENT':
                return Response(
                    {"error": "Access denied. Only students can log in to this application."},
                    status=status.HTTP_403_FORBIDDEN
                )

            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class GoogleAuthAPIView(APIView):
#     def post(self, request):
#         """
#         Handle Google login and return JWT tokens.
#         """
#         google_token = request.data.get("token")
#         if not google_token:
#             return Response({"error": "Google token is required"}, status=status.HTTP_400_BAD_REQUEST)

#         # Verify token with Google
#         google_user_info = self.verify_google_token(google_token)
#         if google_user_info is None:
#             return Response({"error": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST)

#         # Extract user information
#         email = google_user_info.get("email")
#         name = google_user_info.get("name")

#         if not email:
#             return Response({"error": "Google account does not have an email"}, status=status.HTTP_400_BAD_REQUEST)

#         # Check if the user exists or create a new one
#         user, created = User.objects.get_or_create(email=email, user_type='STUDENT', defaults={"name": name, "is_active": True})

#         # Generate JWT token
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)

#         return Response(
#             {
#                 "message": "Login successful",
#                 "access_token": access_token,
#                 "refresh_token": str(refresh),
#                 "user": {
#                     "id": user.id,
#                     "email": user.email,
#                     "name": user.name,
#                 },
#             },
#             status=status.HTTP_200_OK,
#         )

#     def verify_google_token(self, token):
#         """
#         Verifies the Google token using Google's API.
#         """
#         try:
#             response = requests.get(
#                 f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}"
#             )
#             user_info = response.json()
#             if "email" in user_info:
#                 return user_info
#         except Exception as e:
#             print("Error verifying Google token:", str(e))
#         return None


import google.auth
from google.auth.transport.requests import Request
from google.auth.exceptions import GoogleAuthError
from google.oauth2 import id_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

User = get_user_model()

class GoogleAuthAPIView(APIView):
    def post(self, request):
        token = request.data.get("token")

        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Validate the ID token with the Google Auth library
            id_info = id_token.verify_oauth2_token(
                token,
                Request(),  # To create an HTTP request object for the token
                settings.GOOGLE_CLIENT_ID  # Your OAuth2 client ID
            )

            # Get the email and name from the validated token
            email = id_info.get("email")
            name = id_info.get("name")

            # Check if the user exists
            user = User.objects.filter(email=email).first()

            if user:
                # If user exists, check if they are a student
                if user.user_type != 'STUDENT':
                    return Response(
                        {"error": "Access denied. Only students can log in to this application."},
                        status=status.HTTP_403_FORBIDDEN
                    )
            else:
                # Create a new user with STUDENT type
                user = User.objects.create(
                    email=email,
                    name=name,
                    user_type="STUDENT"
                )

            # Generate JWT tokens for the user
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {"email": user.email, "name": user.name, "user_type": user.user_type},
            })
        except GoogleAuthError as e:
            return Response({"error": f"Invalid token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

# from django.shortcuts import render

# def google_auth_test_view(request):
#     return render(request, "oauth_test.html")


import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse

def google_auth_callback(request):
    """Handle Google OAuth callback and exchange the code for tokens."""
    code = request.GET.get("code")

    if not code:
        return JsonResponse({"error": "No authorization code provided"}, status=400)

    # Exchange authorization code for an access token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=data)
    token_data = response.json()

    if "error" in token_data:
        return JsonResponse({"error": token_data["error"]}, status=400)

    # Get user info
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    # Check if user exists in our database
    email = user_info.get("email")
    if email:
        user = User.objects.filter(email=email).first()
        if user and user.user_type != 'STUDENT':
            return JsonResponse({"error": "Access denied. Only students can log in to this application."}, status=403)

    return JsonResponse({"message": "Google Login Successful", "user_info": user_info})

def is_admin(user):
    return user.is_staff or user.is_superuser

# @user_passes_test(is_admin)
def change_user_password(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not new_password or not confirm_password:
            messages.error(request, 'Please fill in all password fields.')
            return render(request, 'admin/change_password.html', {'target_user': user})

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'admin/change_password.html', {'target_user': user})

        # Update the user's password
        user.password = make_password(new_password)
        user.save()

        messages.success(request, f'Password for {user.email} has been updated successfully.')
        return redirect('admin:authuser_user_changelist')

    return render(request, 'admin/change_password.html', {'target_user': user})