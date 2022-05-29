from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from news.models import News


class NewsTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuseroleg',
            email='test@email.com',
            password='password'
        )

        self.news = News.objects.create(
            title='A title',
            content='Some news from test and Hello world!',
            author=self.user,
        )

    def test_string_representation(self):
        news = News(title='A sample title')
        self.assertEqual(str(news), news.title)

    def test_get_absolute_url(self):  # new
        self.assertEqual(self.news.get_absolute_url(), '/news/1/')

    def test_news_content(self):
        self.assertEqual(f'{self.news.title}', 'A title')
        self.assertEqual(f'{self.news.author}', 'testuseroleg')
        self.assertEqual(f'{self.news.content}', 'Some news from test and Hello world!')

    def test_news_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Some news from test and Hello world!')
        self.assertTemplateUsed(response, 'news/home_news_list.html')

    def test_news_detail_view(self):
        response = self.client.get(reverse('home'))
        no_response = self.client.get('/news/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A title')
        self.assertTemplateUsed(response, 'news/home_news_list.html')

    def test_post_update_view(self):
        response = self.client.post(reverse('update_news', args='7'), {
            'title': 'Updated title',
            'content': 'Updated text',
        })
        for post in News.objects.all():
            print(f"---{post.pk}---")
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.post(
            reverse('delete_news', args='6'))
        self.assertEqual(response.status_code, 302)