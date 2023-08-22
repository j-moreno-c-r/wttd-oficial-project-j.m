from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self) :
        data = dict(name='Joao Moreno', cpf='12345678901', email='joaomorenocruzrosa@gmail.com',
                    phone='21-99618-6180')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]
    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, self.email.subject)
    def test_subscription_email_from(self):
        expect = 'turin.atreides@gmail.com'

        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['turin.atreides@gmail.com' , 'joaomorenocruzrosa@gmail.com']

        self.assertEqual(expect, self.email.to)

    def test_subscriptios_email_body(self):
        contents = ['Joao Moreno',
                    '12345678901',
                    'joaomorenocruzrosa@gmail.com',
                    '21-99618-6180',

                    ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
