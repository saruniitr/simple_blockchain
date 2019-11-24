from django.db import models
from django_extensions.db.models import TimeStampedModel


class Role(models.Model):
    tx = models.ForeignKey(
        "Tx", on_delete=models.PROTECT, related_name="role_transactions"
    )


class Entity(models.Model):
    tx = models.ForeignKey(
        "Tx", on_delete=models.PROTECT, related_name="entity_transactions"
    )


class Block(TimeStampedModel):
    header = models.CharField(max_length=256)
    previous_hash = models.CharField(max_length=64)


class Tx(TimeStampedModel):
    tx_type = models.CharField(max_length=16)
    sender = models.ForeignKey(Entity, on_delete=models.PROTECT, related_name="sender")
    recipient = models.ForeignKey(
        Entity, on_delete=models.PROTECT, related_name="recipient"
    )
    data = models.CharField(max_length=4096, blank=True, null=True)
    block = models.ForeignKey(Block, on_delete=models.PROTECT)
