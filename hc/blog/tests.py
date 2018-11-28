from django.test import TestCase
from django.urls import reverse
from .models import Entry

class EntryModelTest(TestCase):
    
    def setUp(self):
        Entry.object.create(
            title = "Sample Blog Entry",
            body = "This is the body of the post"
        )

    def test_entry_context(self):
        entry = Entry.object.get(id=1)
        expected_title = f'{entry.title}'
        expected_body = f'{entry.body}'
        self.assertEqual(expected_title, "Sample Blog Entry")
        self.assertEqual(expected_body, "This is the body of the post")

class BlogPageViewTest(TestCase):

    def test_view_url_by_name(self):
        resp = self.client.get(reverse('hc-blog'))
        self.assertEqual(resp.status_code, 200)
        
    def test_view_url_exists_at_proper_location(self):
        resp = self.client.get('/blog/')
        self.assertEqual(resp.status_code, 200)