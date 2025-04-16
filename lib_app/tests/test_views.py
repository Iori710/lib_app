from django.test import TestCase
from ..views import *
from datetime import datetime

class TestsStatusCord(TestCase):
    def test_status_code(self):
        urls = [
            '/top/',
            '/news/',
            '/search/',
            '/detail/9784764106871/',
            '/review/9784764106871/',
            '/reserve/9784764106871/',
            '/reserving/9784764106871/',
            '/reserved/9784764106871/',
            '/check/',
            '/lending/',
            '/returned/',
            '/reviewing/9784764106871/',
            '/mypage/',
            '/view/reserve/',
            '/view/lending/',
            '/option/username/'
        ]
        
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, '/login/?next=' + url)
                
    def test_code_200(self):
        urls = [
            '/login/',
            '/register/',  
        ]
        
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                
    def test_code_302(self):
        urls = [
            '/logout/' 
        ]
        
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                
    def test_code_404(self):
        urls = [
            '/calendar/9784764106871/'    
        ]
        
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                
class TestsLoginStatusCord(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', password='tester')
        self.client.force_login(user)
        
        library = Library.objects.create(ISBN='9784764106871')
        
        book = Book.objects.create(
            ISBN=library,
            title="title",
            writer="writer",
            publisher="publisher",
            shelf="1F",
            c_code="1920581019002"
        )
        
        Reserve.objects.create(
            user_id=user,
            book_id=book,
            lending_start=datetime.now(),
            lending_end=datetime.now()
        )
        
    def test_login_status_code_200(self):
        urls = [
            '/top/',
            '/news/',
            '/detail/9784764106871/',
            '/review/9784764106871/',
            '/reserve/9784764106871/',
            '/reserved/9784764106871/',
            '/check/',
            '/reviewing/9784764106871/',
            '/mypage/',
            '/view/reserve/',
            '/view/lending/',
            '/option/username/'
        ]
        
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                
    def test_login_status_code_302(self):
        
        urls = [
            '/search/',
        ]
        
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                
    def test_login_status_code_404(self):
        urls = [
            '/reserving/9784764106871/',
            '/lending/',
            '/returned/'
        ]
        
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)