# projects/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, PublicProjectsListView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')

urlpatterns = [
    path('', include(router.urls)),
    path('public-projects/', PublicProjectsListView.as_view(),
         name='public-projects'),
]
