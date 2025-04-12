# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import get_user_model
# from rest_framework.generics import ListAPIView
# from .serializers import (
#     CustomTokenObtainPairSerializer,
#     UserProfileSerializer,
#     FollowSerializer, UserRegistrationSerializer
# )
# from django.shortcuts import get_object_or_404
# from .models import Follow, User
# from django.shortcuts import render
#
# User = get_user_model()
#
#
# class UserRegistrationView(APIView):
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'message': 'User registered successfully',
#                 'access_token': str(refresh.access_token),
#                 'refresh_token': str(refresh)
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class UserLoginView(APIView):
#     def post(self, request):
#         serializer = CustomTokenObtainPairSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.validated_data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class UserLogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         try:
#             refresh_token = request.data['refresh_token']
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#
# class UserListView(ListAPIView):
#     queryset = User.objects.filter(is_active=True)  # Only show active users
#     serializer_class = UserProfileSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         # Add search functionality (optional)
#         queryset = super().get_queryset()
#         search_query = self.request.query_params.get('search', None)
#         if search_query:
#             return queryset.filter(username__icontains=search_query)
#         return queryset
#
#
# class UserProfileView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, user_id):
#         try:
#             user = User.objects.get(id=user_id)
#             serializer = UserProfileSerializer(user)
#             return Response(serializer.data)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     def put(self, request, user_id):
#         if request.user.id != user_id:
#             return Response({'error': 'You can only update your own profile'},
#                             status=status.HTTP_403_FORBIDDEN)
#
#         user = request.user
#         serializer = UserProfileSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class FollowUserView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, user_id):
#         try:
#             user_to_follow = User.objects.get(id=user_id)
#             if request.user == user_to_follow:
#                 return Response({'error': 'You cannot follow yourself'},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             follow, created = Follow.objects.get_or_create(
#                 follower=request.user,
#                 following=user_to_follow
#             )
#
#             if created:
#                 return Response({'message': f'You are now following {user_to_follow.username}'},
#                                 status=status.HTTP_201_CREATED)
#             return Response({'message': 'You already follow this user'},
#                             status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#
#
# class UnfollowUserView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, user_id):
#         try:
#             user_to_unfollow = User.objects.get(id=user_id)
#             follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
#             if follow.exists():
#                 follow.delete()
#                 return Response({'message': f'You have unfollowed {user_to_unfollow.username}'},
#                                 status=status.HTTP_200_OK)
#             return Response({'error': 'You are not following this user'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from .serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
    FollowSerializer
)
from .models import Follow
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

User = get_user_model()


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    queryset = User.objects.filter(is_active=True)  # Only show active users
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Add search functionality (optional)
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            return queryset.filter(username__icontains=search_query)
        return queryset


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        if request.user.id != user_id:
            return Response({'error': 'You can only update your own profile'},
                            status=status.HTTP_403_FORBIDDEN)

        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
            if request.user == user_to_follow:
                return Response({'error': 'You cannot follow yourself'},
                                status=status.HTTP_400_BAD_REQUEST)

            follow, created = Follow.objects.get_or_create(
                follower=request.user,
                following=user_to_follow
            )

            if created:
                return Response({'message': f'You are now following {user_to_follow.username}'},
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'You already follow this user'},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
            follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
            if follow.exists():
                follow.delete()
                return Response({'message': f'You have unfollowed {user_to_unfollow.username}'},
                                status=status.HTTP_200_OK)
            return Response({'error': 'You are not following this user'},
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)




#views for tempolate
class UserRegistrationTemplateView(View):
    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        # You can reuse your existing serializer logic here
        serializer = UserRegistrationSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return redirect('post-list')
        return render(request, 'users/register.html', {'errors': serializer.errors})


class UserLoginTemplateView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.user
            login(request, user)
            return redirect('post-list')
        return render(request, 'users/login.html', {'error': 'Invalid credentials'})


class UserLogoutTemplateView(View):
    def post(self, request):
        logout(request)
        return redirect('login')


class UserProfileTemplateView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_following'] = self.request.user.following.filter(id=self.object.id).exists()
        return context


class UserListTemplateView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            return queryset.filter(username__icontains=search_query)
        return queryset.exclude(id=self.request.user.id)
