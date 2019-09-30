from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductManageViewSet, ProductListViewSet


products_router = DefaultRouter()
products_router.register(r'products', ProductViewSet, base_name='products')
products_router.register(r'productManage', ProductManageViewSet, base_name="productManage")
products_router.register(r'productList', ProductListViewSet, base_name="productList")
