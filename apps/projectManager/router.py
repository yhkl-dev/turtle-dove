from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectConfigureViewSet

project_router = DefaultRouter()
project_router.register(r'projectList', ProjectViewSet, base_name="projectList")
project_router.register(r'projectConfigure', ProjectConfigureViewSet, base_name="projectConfigure")

