from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    LikePostView,
    UnlikePostView,
    CommentListView,
    PostCreateView,
    PostListTemplateView,
    PostDetailTemplateView,
    PostCreateTemplateView,
    PostUpdateTemplateView,
    PostDeleteTemplateView,
)

urlpatterns = [
    path('api/posts/create/', PostCreateView.as_view(), name='post-create'),
    path('api/posts/', PostListView.as_view(), name='post-list'),
    path('api/posts/<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
    path('api/posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('api/posts/<int:post_id>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    path('api/posts/<int:post_id>/comments/', CommentListView.as_view(), name='comment-list'),

    path('', PostListTemplateView.as_view(), name='post-list'),
    path('posts/create/', PostCreateTemplateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailTemplateView.as_view(), name='post-detail'),
    path('posts/<int:pk>/update/', PostUpdateTemplateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteTemplateView.as_view(), name='post-delete'),
]