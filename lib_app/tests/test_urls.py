from django.test import TestCase
from django.urls import reverse, resolve
from ..views import *
from django.contrib.auth.views import LoginView

class TestUrls(TestCase):
    def test_login(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func.view_class, LoginView)
        
    def test_views(self):
        urls = [
            ('logout', Logout),
            ('register', Register),
            ('top', Top),
            ('news_list', NewsList),
            ('search', Search),
            ('check', Check),
            ('lending', BookLending),
            ('returned', BookReturned),
            ('mypage', Mypage),
            ('reserve_view', ReserveView),
            ('lending_view', LendingView),
            ('option', UserOption),
            ('username', UserNameChange),
        ]
        
        for name, view in urls:
            with self.subTest(name=name):
                url = reverse(name)
                self.assertEqual(resolve(url).func, view)

    def test_views_with_int(self):
        urls_with_int = [
            ('news', NewsPage, {'id': 1}),
            ('detail', Detail, {'ISBN': 1234567890}),
            ('review', BookReview, {'ISBN': 1234567890}),
            ('calendar', BookCalendar, {'ISBN': 1234567890}),
            ('reserve', BookReserve, {'ISBN': 1234567890}),
            ('reserving', BookReserving, {'ISBN': 1234567890}),
            ('reserved', BookReserved, {'ISBN': 1234567890}),
            ('reviewing', Reviewing, {'ISBN': 1234567890}),
        ]
        
        for name, view, kwargs in urls_with_int:
            with self.subTest(name=name):
                url = reverse(name, kwargs=kwargs)
                self.assertEqual(resolve(url).func, view)