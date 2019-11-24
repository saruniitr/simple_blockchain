from rest_framework import (
    viewsets,
    permissions,
    status,
    mixins,
    views,
    serializers as drf_serializers,
)

from block import serializers, models


class BlockViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BlockSerializer
    queryset = models.Block.objects.all()
    # permission_classes = (permissions.AllowAny,)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TxSerializer
    queryset = models.Tx.objects.all()
    # permission_classes = (permissions.AllowAny,)
