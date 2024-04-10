from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Project, ProjectMembership
from .serializers import ProjectSerializer, ProjectMembershipSerializer
# Make sure to import your custom permissions
from .permissions import IsProjectOwner, IsProjectManager, IsMember, IsViewer


class PublicProjectPagination(PageNumberPagination):
    page_size = 10  # Set the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class PublicProjectsListView(ListAPIView):
    queryset = Project.objects.filter(is_public=True).order_by('id')
    serializer_class = ProjectSerializer
    pagination_class = PublicProjectPagination


class ProjectViewSet(viewsets.ModelViewSet):
    # queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all projects for the currently authenticated user
        that they own or are assigned to or are public.
        """
        user = self.request.user
        # Adjust the query to include only projects that are either private and owned/assigned to the user,
        # or public but also owned/assigned to the user.
        return Project.objects.filter(
            Q(is_public=False, projectmembership__user=user) |
            Q(owner=user) |
            Q(is_public=True, projectmembership__user=user)
        ).distinct()

    def get_permissions(self):
        """Dynamically assign permissions based on action."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsViewer | IsProjectOwner | IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsProjectManager | IsProjectOwner]
        elif self.action == 'destroy':
            permission_classes = [IsProjectOwner]
        elif self.action in ['add_user', 'remove_user', 'set_user_role']:
            permission_classes = [IsProjectOwner]
        else:
            permission_classes = [IsMember | IsProjectManager | IsProjectOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsProjectOwner])
    def add_user(self, request, pk=None):
        """Add a user to the project with a specified role, or update the role if the user is already a member."""
        project = self.get_object()
        user_id = request.data.get('user_id')
        role = request.data.get('role', 'Viewer')  # Default role

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        membership, created = ProjectMembership.objects.update_or_create(
            project=project, user=user, defaults={'role': role})

        status_msg = 'User added to the project.' if created else 'User role updated.'
        return Response({'status': status_msg, 'role': role}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsProjectOwner])
    def remove_user(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        membership = ProjectMembership.objects.filter(
            project=project, user=user)
        if membership.exists():
            membership.delete()
            return Response({'status': 'User removed from the project'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'User not part of the project'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsProjectOwner])
    def set_user_role(self, request, pk=None):
        """Sets or updates a user's role within the project."""
        project = self.get_object()
        user_id = request.data.get('user_id')
        role = request.data.get('role')
        user = User.objects.get(id=user_id)
        membership, created = ProjectMembership.objects.update_or_create(
            project=project, user=user, defaults={'role': role})
        return Response({'status': 'role set', 'role': membership.role}, status=status.HTTP_200_OK)
