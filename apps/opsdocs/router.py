from rest_framework.routers import DefaultRouter
from .views import OpsdocsViewset


docs_router = DefaultRouter()
docs_router.register(r'opsDocs', OpsdocsViewset, base_name="opsDocs")
