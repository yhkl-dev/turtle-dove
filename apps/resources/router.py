from rest_framework.routers import DefaultRouter
from .views import ResourceViewset, ResourceTypeViewset, ResourceUserViewset


resource_router = DefaultRouter()
resource_router.register(r'resource', ResourceViewset, base_name="resource")
resource_router.register(r'resourceType', ResourceTypeViewset, base_name="resourceType")
resource_router.register(r'resourceUser', ResourceUserViewset, base_name="resourceUser")
