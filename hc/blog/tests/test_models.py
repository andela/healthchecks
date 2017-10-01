from django.test import TestCase, Client
from hc.blog.models import Post
from django.core.urlresolvers import reverse


POST_URL_KWARGS = {'year': 2017, 'month': 'sep', 'day': 30,
                    'slug': 'automation-business-processes'}

class PublishedManagerTestCase(TestCase):
    
    def setUp(self):
        self.post = Post.objects.get(pk=1)

    def test_publishedmanager_published(self):
        published = Post.objects.published()

        ### Assert that a post was published
        self.assert_(len(published) == 1)
        self.assertEqual(published[0], self.post)

class PostModelTestCase(TestCase):
    
    def setUp(self):
        self.post = Post.objects.get(pk=1)

    def test_post_str(self):
        self.assertEqual("{0}".format(self.post), self.post.title)

    def test_post_get_absolute_url(self, fake_ping):
        ### Assert that the published post can be accessed
        self.assertEqual(self.post.get_absolute_url(),
                         reverse('blog-post-detail',
                                 kwargs=POST_URL_KWARGS))
    