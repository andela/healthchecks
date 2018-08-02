from hc.test import BaseTestCase

class ViewTestCase(BaseTestCase):
    def test_it_uses_right_template(self):
        r = self.all_blogs(self, '/blog/')
        self.assertTemplateUsed(r, 'blog/index.html')