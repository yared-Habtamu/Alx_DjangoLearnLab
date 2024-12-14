from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from posts.models import Post, Like
from notifications.models import Notification
from accounts.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from serializers import PostSerializer


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



class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            # Ensure user cannot like the post multiple times
            if Like.objects.get_or_create(user=request.user, post=post):
                return Response({"error": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the like
            Like.objects.create(user=request.user, post=post)

            # Create a notification for the post author
            notification = Notification(
                recipient=post.author,
                actor=request.user,
                verb="liked",
                target_content_type=ContentType.objects.get_for_model(Post),
                target_object_id=post.id,
                target=post
            )
            Notification.objects.create

            return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

class UnLikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            like = Like.objects.filter(user=request.user, post=post).first()

            if like:
                like.delete()
                return Response({"message": "Post unliked successfully."}, status=status.HTTP_204_NO_CONTENT)

            return Response({"error": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, generics.get_object_or_404(Post, pk=pk))
