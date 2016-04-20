from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings

from polls.models import Question, Choice
from django.utils import timezone
import datetime

def create_question(question_text, days):
    """
    Creates a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,
                                   pub_date=time)

def create_choice(choice_text, question):
    return Choice.objects.create(choice_text=choice_text, question=question)

@override_settings(ROOT_URLCONF='tests.view_tests.urls', USE_I18N=True, USE_L10N=False, LANGUAGE_CODE='en')
class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.",
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

@override_settings(ROOT_URLCONF='tests.view_tests.urls', USE_I18N=True, USE_L10N=False, LANGUAGE_CODE='en')
class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future should
        return a 404 not found.
        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        response = self.client.get(reverse('polls:detail',
                                   args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past should
        display the question's text.
        """
        past_question = create_question(question_text='Past Question.',
                                        days=-5)
        response = self.client.get(reverse('polls:detail',
                                   args=(past_question.id,)))
        self.assertContains(response, past_question.question_text,
                            status_code=200)

@override_settings(ROOT_URLCONF='tests.view_tests.urls')
class VoteViewTests(TestCase):
    def test_success_vote(self):
        question = create_question(question_text='question.',
                                          days=0)
        choice1 = create_choice(choice_text='choice1.', question=question)
        choice2 = create_choice(choice_text='choice2.', question=question)
        response = self.client.post(reverse('polls:vote', args=(question.id,)), {'choice': str(choice1.id), })
        self.assertEquals(response.status_code, 302)
    def test_failure_vote(self):
        question = create_question(question_text='question.',
                                          days=0)
        choice1 = create_choice(choice_text='choice1.', question=question)
        response = self.client.post(reverse('polls:vote', args=(question.id,)), {'choice': str(choice1.id+10), })
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'You didn&#39;t select a choice.', status_code=200)
