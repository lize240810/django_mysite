import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

'''
    创建测试
'''


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        '''
            was_published_recent()
            对于其问题的pub_date的返回False是在未来。
        '''
        # 查询16天后提交的问题
        # import ipdb; ipdb.set_trace()
        time = timezone.now().date() + datetime.timedelta(days=16)  # 当前时间添加16天
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

# 启动测试的代码
'''
    python manage.py test polls
    # 寻找polls应用里的测试代码 
    1. 找到TestCase的子类
    2. 创建特殊的数据库供测试使用
    3. 在类中寻找测试方法 以test开头的方法
    4. 刚才在 shell中的代码 拿过来 
    5. 使用assertls() 方法， 发现was_oublished_recently()返回True,而我们期望返回Fasle
'''

    def test_was_published_recently_with_recent_question(self):
        """
        对于其pub_date的问题，was_published_recent()返回True是在最后一天。
        """
        time = timezone.now().date() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    time = timezone.now().date()
    datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
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