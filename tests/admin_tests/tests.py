from django.test import TestCase, modify_settings
from polls.models import Question, Choice
from django.contrib import admin
from django.apps import apps

@modify_settings(
INSTALLED_APPS = {'prepend':['django.contrib.admin','django.contrib.contenttypes']},
)
class PollAdminTest(TestCase):
    def test_question_registration(self):
        self.assertEquals(admin.site.is_registered(Question), True)

@modify_settings(
INSTALLED_APPS = {'remove':'polls', 'prepend':['polls.apps.PollsConfig']},
)
class PollApplicationTest(TestCase):
    def test_poll_application(self):
        self.assertEquals(apps.get_app_config('polls').verbose_name, 'Polls')
