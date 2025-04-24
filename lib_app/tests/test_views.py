from django.test import TestCase, Client
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
                
class TestsLoginPostCord(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='tester')
        self.client.force_login(self.user)
        
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
            user_id=self.user,
            book_id=book,
            lending_start=datetime.now(),
            lending_end=datetime.now()
        )
        
        library2 = Library.objects.create(ISBN='9784012345678')
        book2 = Book.objects.create(
            ISBN=library2,
            title="title",
            writer="writer",
            publisher="publisher",
            shelf="1F",
            c_code="1920123456789"
        )
        Lending.objects.create(
            user_id=self.user,
            book_id=book2,
            lending_start=datetime.now(),
            lending_end=datetime.now(),
            returned=False
        )
                
    def test_post_register_new(self):
        response = self.client.post('/register/', {
            'ISBN':'9784862807069',
            'shelf':'1F',
            'c_code':'1920030013001'
        })
        n_lib = Library.objects.last()
        n_book = Book.objects.last()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(n_lib.ISBN, 9784862807069)
        self.assertEqual(n_lib.stock, 1)
        self.assertEqual(n_book.title, '文系のためのデータサイエンスがわかる本')
        self.assertEqual(n_book.writer.replace(' ',''), '髙橋威知郎1974-')
        self.assertEqual(n_book.publisher, '総合法令出版')
        self.assertEqual(n_book.shelf, '1F')
        self.assertEqual(n_book.c_code, 1920030013001)
    
    def test_post_register_add(self):
        response = self.client.post('/register/', {
            'ISBN':'9784764106871',
            'shelf':'1F',
            'c_code':'1920581019002'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Library.objects.get(ISBN__exact=9784764106871).stock, 2)
        
    def test_post_contact(self):
        response = self.client.post('/contact/', {
            'message':'test'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.first().message, 'test')
        self.assertEqual(Contact.objects.first().created_at, datetime.now().date())
        
    def test_post_check_lending(self):
        session = self.client.session
        response = self.client.post('/check/', {
            'keyword':'1920581019002'
        })
        check_id = Reserve.objects.get(book_id__c_code__exact=1920581019002).id
        
        self.assertRedirects(response, '/lending/')
        self.assertEqual(session['lending_book_id'], check_id)
        
    def test_post_check_returned(self):
        session = self.client.session
        response = self.client.post('/check/', {
            'keyword':'1920123456789'
        })
        check_id = Lending.objects.get(book_id__c_code__exact=1920123456789).id
        
        self.assertRedirects(response, '/returned/')
        self.assertEqual(session['returned_book_id'], check_id)
        
    def test_post_lending(self):
        session = self.client.session
        session['lending_book_id'] = Reserve.objects.get(book_id__c_code__exact=1920581019002).id
        session.save()
        
        response = self.client.post('/lending/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lending.objects.first().id, session['lending_book_id']+1)
        
    def test_post_returned(self):

        session = self.client.session
        session['returned_book_id'] = Lending.objects.get(book_id__c_code__exact=1920123456789).id
        session.save()
        response = self.client.post('/returned/')
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Lending.objects.first().returned)
        
    def test_post_reviewing(self):
        response = self.client.post('/reviewing/9784764106871/', {
            'stars':'3',
            'review':'test'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Review.objects.first().stars, 3)
        self.assertEqual(Review.objects.first().review, 'test')
        
    def test_post_username(self):
        response = self.client.post('/option/username/', {
            'username':'test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.first().username, 'test')
        
    def test_post_password(self):
        response = self.client.post('/option/password/', {
            'old_password':'tester',
            'new_password1':'libraryapp',
            'new_password2':'libraryapp'
        })
        self.assertEqual(response.status_code, 200)
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('libraryapp'))