from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from hc.blog.models import Post


POST_URL_KWARGS = {'year': 2017, 'month': 'sep', 'day': 30,
                    'slug': 'automation-business-processes'}


class AdminMenuURLsTestCase(TestCase):

    def test_admin_menu_option_urls(self):
        url1 = reverse('unpublished-on')
        self.assertTrue(url1.startswith('/unpublished-on/'))
        url2 = reverse('unpublished-off')
        self.assertTrue(url2.startswith('/unpublished-off/'))

class BlogPostDetailURLTestCase(TestCase):
    
    def test_blog_story_detail_url(self):
        url = reverse('blog-post-detail', kwargs=POST_URL_KWARGS)
        
        ### Assert whether the url leads to the particular post
        self.assertEqual(url, '/2017/sep/30/automation-business-processes/')
