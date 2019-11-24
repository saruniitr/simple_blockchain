from django.db import models
from django_extensions.db.models import TimeStampedModel


class Role(models.Model):
    name = models.CharField(max_length=32)


class Entity(models.Model):
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"
    TYPE_CHOICES = ((INTERNAL, INTERNAL), (EXTERNAL, EXTERNAL))
    name = models.CharField(max_length=32)
    entity_type = models.CharField(max_length=12, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name


class Tx(TimeStampedModel):
    tx_type = models.CharField(max_length=16)
    sender = models.ForeignKey(Entity, on_delete=models.PROTECT, related_name="sender")
    recipient = models.ForeignKey(
        Entity, on_delete=models.PROTECT, related_name="recipient"
    )
    data = models.CharField(max_length=4096, blank=True, null=True)


class Block(TimeStampedModel):
    header = models.CharField(max_length=256)
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)
