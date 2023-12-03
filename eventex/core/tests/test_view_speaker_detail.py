from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.core.models import  Speaker

class SpeakerDetailGet(TestCase):
    def setUp(self):
        speaker = Speaker.objects.create(
            name='Grace Hopper',
            slug='grace-hopper',
            photo='https://www.timeforkids.com/wp-content/uploads/2020/08/Grace_003.jpg',
            website='http://hbn.link/hopper-site',
            description='Programadora e almirante'
        )
        self.resp = self.client.get(r('speaker_detail', slug='grace-hopper'))

    def test_get(self):
        """Get should return status 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/speaker_detail.html')

    def test_html(self):
        contents = [
            'Grace Hopper',
            'Programadora e almirante',
            'https://www.timeforkids.com/wp-content/uploads/2020/08/Grace_003.jpg',
            'http://hbn.link/hopper-site',
        ]

        for expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected)

    def test_context(self):
        """Speaker must be in context"""
        speaker = self.resp.context['speaker']
        self.assertIsInstance(speaker, Speaker)

class SpeakerDetailNotFound(TestCase):
    def test_not_found(self):
        response = self.client.get(r('speaker_detail', slug='not-found'))
        self.assertEqual(404, response.status_code)
