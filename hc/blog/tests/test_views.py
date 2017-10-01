from django.core.urlresolvers import reverse
from django.test import TestCase
from hc.blog.models import Post
from hc.blog.views import post_list, post_detail


class PostListViewTestCase(TestCase):
    
    def test_blog_post_list(self):
        response = self.client.get(reverse('blog'))

        ### Assert that the list of blog posts can be viewed
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.templates[0].name, 'blog/articles.html')


class PostDetailViewTestCase(TestCase):
    
    def test_blog_post_detail(self):
        url = reverse('blog-post-detail',
                      kwargs={'year': 2017,
                              'month': 'sep',
                              'day': 30,
                              'slug': 'automation-business-processes'})
        response = self.client.get(url)

        ### Assert the available of a particular post (accessiblity)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                         'blog/post_detail.html')
