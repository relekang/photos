# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from photos.gallery.models import Photo


class PhotoDetailViewTestCase(TestCase):
    fixtures = ['photos/gallery/test_fixtures/gallery.yaml']

    def test_view_without_slug(self):
        response = self.client.get(reverse('gallery:photo_detail'))
        self.assertEqual(response.status_code, 200)

    def test_view_with_slug(self):
        response = self.client.get(reverse('gallery:photo_detail', args=['snowing']))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('gallery:photo_detail', args=['bad-slug']))
        self.assertEqual(response.status_code, 404)


class ArchiveViewTestCase(TestCase):
    fixtures = ['photos/gallery/test_fixtures/gallery.yaml']

    def test_status_code(self):
        response = self.client.get(reverse('gallery:archive'))
        self.assertEqual(response.status_code, 200)

    def test_content(self):
        response = self.client.get(reverse('gallery:archive'))
        self.assertContains(response, 'Snowing')
        self.assertContains(response, Photo.objects.last().archive_thumbnail.url)
