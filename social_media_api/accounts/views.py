from rest_framework import generics  # Import GenericAPIView here
from rest_framework.permissions import IsAuthenticated  # Import IsAuthenticated permission
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer


class FollowUserView(generics.GenericAPIView):  # Use GenericAPIView
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can follow
    serializer_class = UserSerializer

    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.get(id=user_id)  # Get user to follow
            if request.user != user_to_follow:
                request.user.following.add(user_to_follow)  # Add to following list
                return Response({"message": "Successfully followed the user."}, status=status.HTTP_200_OK)
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class UnfollowUserView(generics.GenericAPIView):  # Use GenericAPIView
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can unfollow
    serializer_class = UserSerializer

    def post(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.get(id=user_id)  # Get user to unfollow
            if request.user != user_to_unfollow:
                request.user.following.remove(user_to_unfollow)  # Remove from following list
                return Response({"message": "Successfully unfollowed the user."}, status=status.HTTP_200_OK)
            return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
