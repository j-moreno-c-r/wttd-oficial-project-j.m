from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModel(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Henrique Bastos',
            slug='henrique bastos',
            photo='https://imgs.search.brave.com/IyUkMsEh1B1WQN4mBx1yjM7FO0PiBGzOLx2MaYUsW8U/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9jZG4u/aGFzaG5vZGUuY29t/L3Jlcy9oYXNobm9k/ZS9pbWFnZS91cGxv/YWQvdjE2Nzk4NTY4/Nzg4MzAvaFZwTWNI/Q0N6LmpwZWc_dz00/MDAmaD00MDAmZml0/PWNyb3AmY3JvcD1m/YWNlcyZhdXRvPWNv/bXByZXNzLGZvcm1h/dCZmb3JtYXQ9d2Vi/cA'
        )

    def test_email(self):
        contact = Contact.objects.create( speaker=self.speaker, kind=Contact.EMAIL,
                                          value= 'henrique@bastos.net')
        self.assertTrue(Contact.objects.exists())
    def test_phone(self):
        contact = Contact.objects.create( speaker=self.speaker, kind=Contact.PHONE,
                                          value= '21-996186180')
        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """Contact kind should be limited te E or P"""
        contact = Contact(speaker=self.speaker, kind='A', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact( speaker=self.speaker, kind=Contact.EMAIL, value= 'henrique@bastos.net')
        self.assertEqual('henrique@bastos.net', str(contact))

    class ContactManagerTest(TestCase):
        def setup(self):
            s = Speaker.objects.create(
                name='Henrique Bastos',
                slug='henrique-bastos',
                photo='http://hbn.link/hb-pic'
            )
            s.contact_set.create(kind=Contact.EMAIL, value='henrique@bastos.net')
            s.contact_set.create(kind=Contact.PHONE, value='21-996186180')

        def test_email(self):
            qs = Contact.objects.emails.all()
            expected = ['henrique@bastos.net']
            self.assertQuerySetEqual(qs, expected, lambda o: o.value)

        def test_phones(self):
            qs = Contact.objects.phones.all()
            expected = ['21-996186180']
            self.assertQuerySetEqual(qs, expected, lambda o: o.value)
