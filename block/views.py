from rest_framework import (
    viewsets,
    permissions,
    status,
    mixins,
    views,
    serializers as drf_serializers,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from block import serializers, models


class BlockViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = serializers.BlockSerializer
    queryset = models.Block.objects.all()
    permission_classes = (permissions.AllowAny,)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TxSerializer
    queryset = models.Tx.objects.all()
    permission_classes = (permissions.AllowAny,)


class TransactionVerifyViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.TxVerifySerializer
    queryset = models.Block.objects.all()
    permission_classes = (permissions.AllowAny,)

    @action(methods=["post"], detail=False)
    def verify(self, request, **kwargs):
        tx_hash = request.data["tx_hash"]
        for obj in models.Block.objects.all():
            if tx_hash == obj.calc_block_hash_sig():
                return Response(
                    {"tx_hash": tx_hash, "status": "Transaction is valid"},
                    status=status.HTTP_200_OK,
                )

        return Response(
            {"tx_hash": tx_hash, "status": "Transaction doesn't exist on the chain"},
            status=status.HTTP_200_OK,
        )
