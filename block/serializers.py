import hashlib
import json
import zmq

from block import models
from rest_framework import serializers

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://server_node:5555")

def create_block(tx_obj):
    data = json.dumps({
        "id": tx_obj.id,
        "sender": tx_obj.sender.id,
        "recipient": tx_obj.recipient.id,
        "role": tx_obj.role.id,
        "data": tx_obj.data,
    }, sort_keys=True)

    last_block = models.Block.objects.last()
    b = models.Block.objects.create(
        header="version 0.1,01,01", previous_hash=last_block.hash, hash="0"
    )
    key = hashlib.sha256()
    key.update(str(b.id).encode("utf-8"))
    key.update(str(b.created).encode("utf-8"))
    key.update(str(data).encode("utf-8"))
    key.update(str(b.previous_hash).encode("utf-8"))
    b.hash = key.hexdigest()
    b.save()

    return b.calc_block_hash_sig()


def send_tx_to_node(tx):
    data = json.dumps({
        "id": tx.id,
        "sender": tx.sender.id,
        "recipient": tx.recipient.id,
        "role": tx.role.id,
        "data": tx.data,
    }, sort_keys=True)

    socket.send_string(data)
    message = socket.recv()


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Block
        fields = "__all__"

    def create(self, *args, **kwargs):
        obj = super().create(*args, **kwargs)
        return obj


class TxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tx
        fields = "__all__"

    def create(self, *args, **kwargs):
        obj = super().create(*args, **kwargs)
        obj.refresh_from_db()

        obj.tx_hash = create_block(obj)
        obj.save()

        # TODO: Move block creation to server_node
        # At the moment we only send a message
        send_tx_to_node(obj)
        return obj


class TxVerifySerializer(serializers.Serializer):
    tx_hash = serializers.CharField()
