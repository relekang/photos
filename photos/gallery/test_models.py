# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils.safestring import SafeText
from photos.gallery.models import Photo


class PhotoTestCase(TestCase):
    fixtures = ['photos/gallery/test_fixtures/gallery.yaml']

    def setUp(self):
        self.object = Photo.objects.last()

    def test_slug(self):
        self.object.slug = None
        self.object.save()
        self.assertEqual(self.object.slug, 'snowing')

        self.object.slug = ''
        self.object.save()
        self.assertEqual(self.object.slug, 'snowing')

    def test_properties(self):
        self.assertEqual(str(self.object), 'Snowing')
        self.assertEqual(self.object.slug, 'snowing')
        self.assertEqual(self.object.camera, 'NIKON D300')
        self.assertEqual(self.object.lens, '70.0-200.0 mm f/2.8')
        self.assertEqual(self.object.aperture, 2.8)
        self.assertEqual(self.object.focal_length, 70)
        self.assertEqual(self.object.exposure_time, '1/100')
        self.assertEqual(self.object.iso, 200)

    def test_large_thumbnail(self):
        thumb = self.object.large_thumbnail
        self.assertIsNotNone(thumb.url)
        self.assertEqual(thumb.x, 3000)

    def test_square_thumbnail(self):
        thumb = self.object.square_thumbnail
        self.assertIsNotNone(thumb.url)
        self.assertEqual(thumb.x, 1000)
        self.assertEqual(thumb.y, 1000)

    def test_admin_thumbnail(self):
        thumb = self.object.admin_thumbnail
        self.assertTrue(isinstance(thumb, SafeText))
        self.assertTrue('<img src="/uploads/cache/' in thumb)
        self.assertTrue('" alt="Snowing" />' in thumb)
