from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .models import NetworkNode
from .serializers import NetworkNodeSerializer


class NetworkNodeViewSet(ModelViewSet):
    """CRUD для звена сети с фильтрацией по стране."""

    queryset = NetworkNode.objects.select_related("contact", "supplier").all()
    serializer_class = NetworkNodeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("contact__country",)
