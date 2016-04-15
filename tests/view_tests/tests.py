from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings

@override_settings(ROOT_URLCONF='tests.view_tests.urls', USE_I18N=True, USE_L10N=False, LANGUAGE_CODE='en')
class IndexViewTests(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'Hello World', status_code=200)
