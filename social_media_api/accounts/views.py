# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework.permissions import IsAuthenticated
# from .models import CustomUser
# from .serializers import UserSerializer
# from rest_framework import status
#
#
# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             token = Token.objects.get(user=user)
#             return Response({'token': str(token)}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class LoginView(APIView):
#     def post(self, request):
#         from django.contrib.auth import authenticate
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({'token': str(token)}, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class UserViewSet(ModelViewSet):
    """
    A ViewSet for handling user registration, listing, and profile updates.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Set permissions based on the action
        if self.action in ['create', 'list']:
            return [AllowAny()]
        return [IsAuthenticated()]
