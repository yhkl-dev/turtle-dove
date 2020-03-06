from rest_framework.routers import DefaultRouter
from .views import ZabbixHostStatusViewset, ProductHostStatusViewset, ZabbixHostListViewset

zabbix_router = DefaultRouter()
zabbix_router.register(r'zabbixStatus', ZabbixHostStatusViewset, basename="zabbixStatus")
zabbix_router.register(r'zabbixProduct', ProductHostStatusViewset, basename="zabbixProduct")
zabbix_router.register(r'zabbixHostList', ZabbixHostListViewset, basename="zabbixHostList")
