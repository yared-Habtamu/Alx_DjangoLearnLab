from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from accounts.models import CustomUser

class FeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated to view the feed

    def get_queryset(self):
        # Get the current user
        user = self.request.user

        # Get the users that the current user is following
        following_users = user.following.all()

        # Get posts from users that the current user follows
        # Order by created_at to get the most recent posts first
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

    def get(self, request, *args, **kwargs):
        # This will return the feed of posts from followed users
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
