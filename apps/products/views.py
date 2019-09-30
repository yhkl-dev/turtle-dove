from rest_framework import mixins, viewsets, response, status, serializers,permissions
from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter
from rest_framework.response import Response
from resources.models import Resource
from django.db.models import Q


class ProductViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    返回指定业务线信息

    list:
    返回业务线列表

    update:
    更新业务线信息

    destroy:
    删除业务线记录

    create:
    创建业务线资源

    partial_update:
    更新部分字段
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    extra_perms_map = {
        "GET": ["products.view_product"]
    }
    filter_class = ProductFilter
    filter_fields = ("pid",)

    def destroy(self, request, *args, **kwargs):
        ret = {"status": 0}
        instance = self.get_object()
        if instance.pid == 0:
            # 顶级业务线
            # 查找二级级业务线
            if Product.objects.filter(pid__exact=instance.id).count() != 0:
                ret["status"] = 1
                ret["errmsg"] = "该业务下还有二级业务线"
                return response.Response(ret, status=status.HTTP_200_OK)
        else:
            # 二级业务线
            if Resource.objects.filter(server_purpose__id__exact=instance.id).count() != 0:
                ret["status"] = 1
                ret["errmsg"] = "该分组下还有产品线，不能删除"
                return response.Response(ret, status=status.HTTP_200_OK)

        self.perform_destroy(instance)
        return response.Response(ret, status=status.HTTP_200_OK)

class ProductListViewSet(viewsets.ReadOnlyModelViewSet, mixins.ListModelMixin):
    """
    retrieve:
    返回指定业务线信息

    list:
    返回业务线列表

    """
    # queryset = Product.objects.values_list('id', 'service_name', 'pid').filter(~Q(pid=0))
    # serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.Serializer
    # extra_perms_map = {
    #     "GET": ["products.view_product"]
    # }
    # filter_class = ProductFilter
    # filter_fields = ("pid",)

    def list(self, request, *args, **kwargs):
        # return Response(data, status=status.HTTP_200_OK)
        return  Response(Product.objects.values('id', 'service_name').filter(~Q(pid=0)), status=status.HTTP_200_OK)


class ProductManageViewSet(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    list:
    业务线管理
    """
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        data = self.get_products()
        return response.Response(data)

    def get_products(self):
        ret = []
        for obj in self.queryset.filter(pid=0):
            node = self.get_node(obj)
            node["children"] = self.get_children(obj.id)
            ret.append(node)
        return ret

    def get_children(self, pid):
        ret = []
        for obj in self.queryset.filter(pid=pid):
            ret.append(self.get_node(obj))
        return ret

    def get_node(self, product_obj):
        node = {}
        node["id"] = product_obj.id
        node["label"] = product_obj.service_name
        node["pid"] = product_obj.pid
        return node
