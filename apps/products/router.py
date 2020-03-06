from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductManageViewSet, ProductListViewSet


products_router = DefaultRouter()
products_router.register(r'products', ProductViewSet, basename='products')
products_router.register(r'productManage', ProductManageViewSet, basename="productManage")
products_router.register(r'productList', ProductListViewSet, basename="productList")
