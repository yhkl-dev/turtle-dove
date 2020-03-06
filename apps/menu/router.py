from rest_framework.routers import DefaultRouter
from .views import MenuViewset, GroupMenuViewset

menu_router = DefaultRouter()
menu_router.register(r'menus', MenuViewset, basename="menus")
menu_router.register(r'groupmenus', GroupMenuViewset, basename="groupmenus")
