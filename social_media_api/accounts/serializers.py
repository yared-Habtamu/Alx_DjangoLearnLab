from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# Get the user model dynamically
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()  # Explicitly declare the password field

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        # Create a new user using `get_user_model().objects.create_user`
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

        # Handle additional fields (bio, profile_picture)
        user.bio = validated_data.get('bio', '')
        user.profile_picture = validated_data.get('profile_picture', None)
        user.save()

        # Generate and attach a token to the new user
        Token.objects.create(user=user)

        return user
