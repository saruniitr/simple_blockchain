from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from block import models


class TxViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_tx_create_block_create(self):
        response = self.client.get(reverse("tx-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        txs = response.json()
        self.assertEqual(len(txs), 1)
        blocks = self.client.get(reverse("block-list")).json()
        self.assertEqual(len(txs), len(blocks))

        sender = models.Entity.objects.get(name="Sender")
        recipient = models.Entity.objects.get(name="Receiver")

        for i in range(5):
            data = {
                "tx_type": "INTERNAL",
                "sender": sender.id,
                "recipient": recipient.id,
                "data": f"Transaction {i+1}"
            }
            response = self.client.post(reverse("tx-list"), data=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse("tx-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        txs = response.json()
        self.assertEqual(len(txs), 6)

        blocks = self.client.get(reverse("block-list")).json()
        self.assertEqual(len(txs), len(blocks))
