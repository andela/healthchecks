from hc.test import BaseTestCase


class PostTestCase(BaseTestCase):

    def test_it_renders_blog_page(self):
        r = self.client.get('/blog/')
        self.assertEqual(r.status_code, 200)

    def test_it_uses_right_template(self):
        r = self.client.get('/blog/')
        self.assertTemplateUsed(r, 'blog/index.html')
