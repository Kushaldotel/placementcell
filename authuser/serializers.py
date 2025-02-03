from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Authenticate the user
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return {
                'email': user.email,
                'name': user.name,
                'user_type': user.user_type,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }
        raise serializers.ValidationError('Invalid email or password.')