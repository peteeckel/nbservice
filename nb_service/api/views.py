from netbox.api.viewsets import NetBoxModelViewSet

from nb_service import models
from nb_service import filters
from . import serializers

class ICViewSet(NetBoxModelViewSet):
    queryset = models.IC.objects.all()
    serializer_class = serializers.ICSerializer
    filterset_class = filters.ICFilter


class ServiceViewSet(NetBoxModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer

class ApplicationViewSet(NetBoxModelViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer

class RelationViewSet(NetBoxModelViewSet):
    queryset = models.Relation.objects.all()
    serializer_class = serializers.RelationSerializer
