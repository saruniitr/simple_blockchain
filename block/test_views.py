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
        role = models.Role.objects.first()

        for i in range(5):
            data = {
                "tx_type": "INTERNAL",
                "sender": sender.id,
                "recipient": recipient.id,
                "role": role.id,
                "data": f"Transaction {i+1}",
            }
            response = self.client.post(reverse("tx-list"), data=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse("tx-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        txs = response.json()
        self.assertEqual(len(txs), 6)

        blocks = self.client.get(reverse("block-list")).json()
        self.assertEqual(len(txs), len(blocks))

    def test_medical_prescription_flow(self):
        doctor = models.Role.objects.create(name="Doctor")
        patient = models.Role.objects.create(name="Patient")
        employer = models.Role.objects.create(name="Employer")
        insurer = models.Role.objects.create(name="Insurer")

        gp_practice = models.Entity.objects.create(
            name="Care practice", entity_type="INTERNAL"
        )
        gp_patient = models.Entity.objects.create(
            name="Patient1", entity_type="INTERNAL"
        )
        workplace = models.Entity.objects.create(
            name="Block Labs", entity_type="EXTERNAL"
        )
        ins_workplace = models.Entity.objects.create(
            name="ABC Insurers", entity_type="EXTERNAL"
        )

        transactions = [
            {
                "tx_type": "INTERNAL",
                "sender": gp_practice.id,
                "recipient": gp_patient.id,
                "role": doctor.id,
                "data": "Prescription for Cold",
            },
            {
                "tx_type": "INTERNAL",
                "sender": gp_practice.id,
                "recipient": gp_patient.id,
                "role": doctor.id,
                "data": "Prescription for Viral illness",
            },
            {
                "tx_type": "EXTERNAL",
                "sender": gp_patient.id,
                "recipient": workplace.id,
                "role": patient.id,
                "data": "Sick leave",
            },
            {
                "tx_type": "INTERNAL",
                "sender": workplace.id,
                "recipient": ins_workplace.id,
                "role": employer.id,
                "data": "Insurance claim for Patient 1",
            },
            {
                "tx_type": "INTERNAL",
                "sender": workplace.id,
                "recipient": ins_workplace.id,
                "role": employer.id,
                "data": "Insurance claim for Patient 2",
            },
            {
                "tx_type": "INTERNAL",
                "sender": ins_workplace.id,
                "recipient": gp_practice.id,
                "role": insurer.id,
                "data": "Request for Patient 1 visits",
            },
        ]

        for tx_data in transactions:
            response = self.client.post(reverse("tx-list"), data=tx_data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(doctor.tx_set.all().count(), 2)
        self.assertEqual(patient.tx_set.all().count(), 1)
        self.assertEqual(employer.tx_set.all().count(), 2)
        self.assertEqual(insurer.tx_set.all().count(), 1)
