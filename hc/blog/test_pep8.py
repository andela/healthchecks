from django.test import TestCase
import pycodestyle

class TestCodeStyle(TestCase):

	def test_conformance(self):
		"""Test whether our code conforms to PEP-8 style guide.

		"""

		style = pycodestyle.StyleGuide(quiet=True)
		# Confirming if models.py and views.py files conform to PEP-8
		result = style.check_files(['models.py', 'views.py'])
		self.assertEqual(result.total_errors, 0,
						"Found code style errors and warnings.")