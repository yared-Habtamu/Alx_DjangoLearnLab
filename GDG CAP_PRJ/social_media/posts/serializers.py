from rest_framework import serializers
from .models import Post, Comment, Like
from users.serializers import UserProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    image = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'created_at', 'image', 'updated_at', 'likes_count', 'comments_count')
        read_only_fields = ('user', 'created_at', 'updated_at', 'likes_count', 'comments_count')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'content', 'created_at')
        read_only_fields = ('user', 'post', 'created_at')


class LikeSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'created_at')
        read_only_fields = ('user', 'post', 'created_at')
