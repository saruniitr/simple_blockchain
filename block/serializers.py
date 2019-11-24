import hashlib
from block import models
from rest_framework import serializers


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Block
        fields = "__all__"

    def create(self, *args, **kwargs):
        obj = super().create(*args, **kwargs)
        print("Block serializer create")
        return obj

class TxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tx
        fields = "__all__"

    def create(self, *args, **kwargs):
        obj = super().create(*args, **kwargs)
        print(f"Tx serializer create, {self.data}")
        return obj
