from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from notifications.models import Notification

class NotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user, read=False)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Mark notifications as read
        for notification in queryset:
            notification.read = True
            notification.save()

        return Response({"notifications": queryset.values()}, status=status.HTTP_200_OK)
