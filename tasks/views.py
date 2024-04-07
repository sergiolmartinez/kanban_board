from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
# Import the IsAuthenticated permission class
from rest_framework.permissions import IsAuthenticated
import logging
logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # Ensure that only authenticated users can access this viewset
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        logger.debug(f"Creating task for user: {self.request.user}")
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.debug(f"Serializer errors: {serializer.errors}")
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        logger.debug(
            f"Inside perform_create, setting owner as {self.request.user}")

        serializer.save(owner=self.request.user)
