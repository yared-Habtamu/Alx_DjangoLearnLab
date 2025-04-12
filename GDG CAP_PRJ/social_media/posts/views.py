# from rest_framework.pagination import PageNumberPagination
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.generics import CreateAPIView
# from rest_framework.permissions import IsAuthenticated
# from .models import Post, Comment, Like
# from .serializers import PostSerializer, CommentSerializer, LikeSerializer
# from users.models import User
# from rest_framework.parsers import MultiPartParser, FormParser
#
#
# class PostCreateView(CreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]  # Add this for file uploads
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class PostListView(APIView):  # only get& post to list and create post functionality
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     pagination_class = PageNumberPagination
#
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         posts = Post.objects.all().order_by('-created_at')
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = PostSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class PostDetailView(APIView):  # handle all request cases
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self, post_id):
#         try:
#             return Post.objects.get(id=post_id)
#         except Post.DoesNotExist:
#             return None
#
#     def get(self, request, post_id):
#         post = self.get_object(post_id)
#         if post is None:
#             return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     def put(self, request, post_id):
#         post = self.get_object(post_id)
#         if post is None:
#             return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         if post.user != request.user:
#             return Response({'error': 'You can only edit your own posts'}, status=status.HTTP_403_FORBIDDEN)
#
#         serializer = PostSerializer(post, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, post_id):
#         post = self.get_object(post_id)
#         if post is None:
#             return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         if post.user != request.user:
#             return Response({'error': 'You can only delete your own posts'}, status=status.HTTP_403_FORBIDDEN)
#
#         post.delete()
#         return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#
#
# class LikePostView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, post_id):
#         try:
#             post = Post.objects.get(id=post_id)
#             like, created = Like.objects.get_or_create(user=request.user, post=post)
#
#             if created:
#                 return Response({'message': 'Post liked'}, status=status.HTTP_201_CREATED)
#             return Response({'message': 'You already liked this post'}, status=status.HTTP_200_OK)
#         except Post.DoesNotExist:
#             return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
#
#
# class UnlikePostView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, post_id):
#         try:
#             post = Post.objects.get(id=post_id)
#             like = Like.objects.filter(user=request.user, post=post)
#
#             if like.exists():
#                 like.delete()
#                 return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
#             return Response({'error': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)
#         except Post.DoesNotExist:
#             return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
#
#
# class CommentListView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, post_id):
#         try:
#             post = Post.objects.get(id=post_id)
#             comments = post.comments.all().order_by('-created_at')
#             serializer = CommentSerializer(comments, many=True)
#             return Response(serializer.data)
#         except Post.DoesNotExist:
#             return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     def post(self, request, post_id):
#         try:
#             post = Post.objects.get(id=post_id)
#             serializer = CommentSerializer(data=request.data, context={'request': request})
#             if serializer.is_valid():
#                 serializer.save(user=request.user, post=post)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Post.DoesNotExist:
#             return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from users.models import User
from rest_framework.parsers import MultiPartParser, FormParser

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Add this for file uploads

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostListView(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, post_id):
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return None

    def get(self, request, post_id):
        post = self.get_object(post_id)
        if post is None:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_id):
        post = self.get_object(post_id)
        if post is None:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if post.user != request.user:
            return Response({'error': 'You can only edit your own posts'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        post = self.get_object(post_id)
        if post is None:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if post.user != request.user:
            return Response({'error': 'You can only delete your own posts'},
                            status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            like, created = Like.objects.get_or_create(user=request.user, post=post)

            if created:
                return Response({'message': 'Post liked'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'You already liked this post'}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            like = Like.objects.filter(user=request.user, post=post)

            if like.exists():
                like.delete()
                return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
            return Response({'error': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


class CommentListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            comments = post.comments.all().order_by('-created_at')
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            serializer = CommentSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(user=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


# class based post template views
class PostListTemplateView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked_posts'] = self.request.user.likes.values_list('post_id', flat=True)
        return context


class PostDetailTemplateView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
        context['is_liked'] = self.object.likes.filter(user=self.request.user).exists()
        return context


class PostCreateTemplateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['content', 'image']

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostUpdateTemplateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['content', 'image']

    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostDeleteTemplateView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)
