import hashlib

from django.db import models
from django_extensions.db.models import TimeStampedModel


class Role(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Entity(models.Model):
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"
    TYPE_CHOICES = ((INTERNAL, INTERNAL), (EXTERNAL, EXTERNAL))
    name = models.CharField(max_length=32)
    entity_type = models.CharField(max_length=12, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name


class Tx(TimeStampedModel):
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"
    PRIVATE = "PRIVATE"
    TX_CHOICES = ((INTERNAL, INTERNAL), (EXTERNAL, EXTERNAL), (PRIVATE, PRIVATE))
    tx_type = models.CharField(max_length=16, choices=TX_CHOICES)
    sender = models.ForeignKey(Entity, on_delete=models.PROTECT, related_name="sender")
    recipient = models.ForeignKey(
        Entity, on_delete=models.PROTECT, related_name="recipient"
    )
    data = models.CharField(max_length=4096, blank=True, null=True)
    tx_hash = models.CharField(max_length=64, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    def __str__(self):
        return f"transaction_{self.tx_type}"


class Block(TimeStampedModel):
    header = models.CharField(max_length=256)
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)

    def calc_block_hash_sig(self):
        key = hashlib.sha256()
        key.update(str(self.previous_hash).encode("utf-8"))
        key.update(str(self.hash).encode("utf-8"))
        return key.hexdigest()
