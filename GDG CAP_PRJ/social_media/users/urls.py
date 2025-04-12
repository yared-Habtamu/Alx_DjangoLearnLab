from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    FollowUserView,
    UnfollowUserView,
    UserListView,

    UserRegistrationTemplateView,
    UserLoginTemplateView,
    UserLogoutTemplateView,
    UserProfileTemplateView,
    UserListTemplateView,

)

urlpatterns = [
    path('api/auth/register/', UserRegistrationView.as_view(), name='register'),
    path('api/auth/login/', UserLoginView.as_view(), name='login'),
    path('api/auth/logout/', UserLogoutView.as_view(), name='logout'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
    path('api/<int:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('api/<int:user_id>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),

    # Template rendering URLs
    path('register/', UserRegistrationTemplateView.as_view(), name='register'),
    path('login/', UserLoginTemplateView.as_view(), name='login'),
    path('logout/', UserLogoutTemplateView.as_view(), name='logout'),
    path('users/', UserListTemplateView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserProfileTemplateView.as_view(), name='user-profile'),
]