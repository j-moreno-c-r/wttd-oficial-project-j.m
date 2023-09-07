from django.test import TestCase
from datetime import datetime

from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='João Moreno',
            cpf='12345678901',
            email='joaomorenocruzrosa@gmail.com',
            phone='21-99618-6180',
        )
        self.obj.save()
    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_create(self):
        """Subscription must have an auto created at attr."""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('João Moreno', str(self.obj))
