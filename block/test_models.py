import json

from django.test import TestCase
from block import models


class TxTestCase(TestCase):
    def test_block_creation_with_tx_create(self):
        initial_count = models.Tx.objects.all().count()
        self.assertEqual(initial_count, 1)
        self.assertEqual(models.Block.objects.all().count(), initial_count)

        sender = models.Entity.objects.get(name="Sender")
        recipient = models.Entity.objects.get(name="Receiver")

        for i in range(5):
            models.Tx.objects.create(
                tx_type="INTERNAL",
                sender=sender,
                recipient=recipient,
                data=json.dumps({"data": f"Transaction {i+1}"}, sort_keys=True),
            )
        self.assertEqual(models.Tx.objects.all().count(), 6)
        self.assertEqual(models.Block.objects.all().count(), 1)
