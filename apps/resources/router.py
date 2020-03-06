from rest_framework.routers import DefaultRouter
from .views import ResourceViewset, ResourceTypeViewset, ResourceUserViewset


resource_router = DefaultRouter()
resource_router.register(r'resource', ResourceViewset, basename="resource")
resource_router.register(r'resourceType', ResourceTypeViewset, basename="resourceType")
resource_router.register(r'resourceUser', ResourceUserViewset, basename="resourceUser")
