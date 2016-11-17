from django.test import TestCase
import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Question
from django.urls import reverse
# Create your tests here.


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_quesiton(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question=Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_quesiton(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_quesiton(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, day):
    time = timezone.now() + datetime.timedelta(days=day)
    return Question.objects.create(question_text=question_text, pub_date=time)



class QuestionViewTests(TestCase):
    def create_question(question_text, days):
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)

    def test_index_view_with_no_questions(self):
        response = self.client.get(reverse('poos:index'))
        self.assertIs(response.status_code, 200)
        self.assertContains(response, "No poos are available")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_index_view_with_a_past_question(self):
        create_question(question_text="Past question", day=-30)
        response = self.client.get(reverse('poos:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])

    def test_index_view_with_a_future_question(self):
        create_question(question_text="future question", day=30)
        response = self.client.get(reverse("poos:index"))
        self.assertContains(response, "No poos are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_future_and_an_old_question(self):
        create_question(question_text="future question", day=30)
        create_question(question_text="Past question", day=-30)
        response = self.client.get(reverse("poos:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])


class QuestionIndexDetailTests(TestCase):

    def test_detail_view_with_a_future_question(self):
        future_question = create_question(question_text="future question", day=5)

        response = self.client.get(reverse('poos:results', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)