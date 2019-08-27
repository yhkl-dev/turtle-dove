from .models import Opsdocs
from .serializers import OpsDocsSerialziers
from rest_framework import viewsets
from TurtleDove.paginations import Pagination



class OpsdocsViewset(viewsets.ModelViewSet):
    queryset = Opsdocs.objects.all()
    serializer_class = OpsDocsSerialziers
    pagination_class = Pagination