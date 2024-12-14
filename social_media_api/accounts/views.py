from rest_framework import generics  # For GenericAPIView
from rest_framework import permissions  # For ensuring the user is authenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer


class UserListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can access
    serializer_class = UserSerializer

    def get(self, request):
        users = CustomUser.objects.all()  # Fetch all users
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# View for following a user
class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can follow
    serializer_class = UserSerializer

    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.get(id=user_id)  # Get the user to follow by ID
            if request.user != user_to_follow:  # Ensure the user is not following themselves
                request.user.following.add(user_to_follow)  # Add to following list
                return Response({"message": "Successfully followed the user."}, status=status.HTTP_200_OK)
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


# View for unfollowing a user
class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can unfollow
    serializer_class = UserSerializer

    def post(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.get(id=user_id)  # Get the user to unfollow by ID
            if request.user != user_to_unfollow:  # Ensure the user is not unfollowing themselves
                request.user.following.remove(user_to_unfollow)  # Remove from following list
                return Response({"message": "Successfully unfollowed the user."}, status=status.HTTP_200_OK)
            return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
