from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Feedback
from .serializers import FeedbackSerializer
from .permissions import IsAdmin, IsOwnerOrAdmin


class FeedbackAPIView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]


class FeedbackDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [AllowAny()]
