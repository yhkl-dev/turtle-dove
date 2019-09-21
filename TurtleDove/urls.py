"""ops_manager_v2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from users.router import user_router
from groups.router import group_router
from menu.router import menu_router
from permissions.router import permission_router
from products.router import products_router
from zabbix.router import zabbix_router
from resources.router import resource_router
from opsdocs.router import docs_router
from serverreports.router import reports_router
from workorder.router import work_order_router
from workorder.views import download_work_file
from serverreports.views import download_file
from autotask.router import tasks_router
from projectManager.router import project_router
router = DefaultRouter()

router.registry.extend(user_router.registry)
router.registry.extend(group_router.registry)
router.registry.extend(menu_router.registry)
router.registry.extend(permission_router.registry)
router.registry.extend(resource_router.registry)
router.registry.extend(products_router.registry)
router.registry.extend(zabbix_router.registry)
router.registry.extend(docs_router.registry)
router.registry.extend(reports_router.registry)
router.registry.extend(tasks_router.registry)
router.registry.extend(work_order_router.registry)
router.registry.extend(project_router.registry)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^download/', download_file),
    url(r'^downloadWorkOrderFile/', download_work_file),
    url(r'^docs/', include_docs_urls("ykyk")),
]
