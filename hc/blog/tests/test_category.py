from hc.test import BaseTestCase
from hc.blog.models import Category


class CategoryTestCase(BaseTestCase):

    def test_it_can_create_category(self):
        category = Category()
        category.title = "Technology"
        category.save()

        all_categories = Category.objects.all()
        # Check if category is saved
        self.assertEquals(len(all_categories), 1)
        # Check if title is the same
        saved_category = all_categories[0]
        self.assertEqual(saved_category.title, category.title)
