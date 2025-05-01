from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from ..models import *

class TestModels(TestCase):
    def test_field_library(self):
        library = Library()
        self.assertEqual(library._meta.get_field('ISBN').primary_key, True)
        self.assertEqual(library._meta.get_field('ISBN').default, 9784000000000)
        
        self.assertEqual(library._meta.get_field('stock').default, 1)
        
    def test_field_book(self):
        book = Book()
        self.assertEqual(book._meta.get_field('ISBN').related_model, Library)
        self.assertEqual(book._meta.get_field('title').max_length, 100)
        self.assertEqual(book._meta.get_field('writer').max_length, 50)
        self.assertEqual(book._meta.get_field('publisher').max_length, 50)
        self.assertEqual(book._meta.get_field('shelf').max_length, 50)
        self.assertEqual(book._meta.get_field('c_code').default, 1920000000000)
        
    def test_field_review(self):
        review = Review()
        self.assertEqual(review._meta.get_field('user_id').related_model, User)
        self.assertEqual(review._meta.get_field('ISBN').related_model, Library)
        self.assertEqual(review._meta.get_field('stars').default, 1)
        self.assertEqual(review._meta.get_field('stars').validators[0].limit_value, 1)
        self.assertEqual(review._meta.get_field('stars').validators[1].limit_value, 5)
        self.assertTrue(review._meta.get_field('review').blank)
        self.assertTrue(review._meta.get_field('review').null)
        
    def test_field_reserve(self):
        reserve = Reserve()
        self.assertEqual(reserve._meta.get_field('user_id').related_model, User)
        self.assertEqual(reserve._meta.get_field('book_id').related_model, Book)
        
    def test_field_lending(self):
        lending = Lending()
        self.assertFalse(lending._meta.get_field('returned').default)
        
    def test_field_news(self):
        news = News()
        self.assertEqual(news._meta.get_field('title').max_length, 100)
        self.assertFalse(news._meta.get_field('content').blank)
        self.assertFalse(news._meta.get_field('content').null)
        
    def test_field_contact(self):
        contact = Contact()
        self.assertEqual(contact._meta.get_field('user_id').related_model, User)
        self.assertFalse(contact._meta.get_field('message').blank)
        self.assertFalse(contact._meta.get_field('message').null)
        
    def test_saving_and_retrieving_Library(self):
        library = Library.objects.create(ISBN=9784012345678, stock=1)
        retrieved_library = Library.objects.first()
        self.assertEqual(retrieved_library, library)
        
    def test_saving_and_retrieving_Book(self):
        library = Library.objects.create(ISBN=9784012345678, stock=1)
        book = Book.objects.create(ISBN=library, title='Test Book', writer='Test Author', publisher='Test Publisher', shelf='Test Shelf', c_code=1920123456789)
        
        retrieved_book = Book.objects.first()
        self.assertEqual(retrieved_book, book)
        
    def test_saving_and_retrieving_Review(self):
        user = User.objects.create(username='testuser', password='testpassword')
        library = Library.objects.create(ISBN=9784012345678, stock=1)
        Book.objects.create(ISBN=library, title='Test Book', writer='Test Author', publisher='Test Publisher', shelf='Test Shelf', c_code=1920123456789)
        
        review = Review.objects.create(user_id=user, ISBN=library, stars=5, review='Great book!')
        
        retrieved_review = Review.objects.first()
        self.assertEqual(retrieved_review, review)
        
    def test_saving_and_retrieving_Reserve(self):
        user = User.objects.create(username='testuser', password='testpassword')
        library = Library.objects.create(ISBN=9784012345678, stock=1)
        book = Book.objects.create(ISBN=library, title='Test Book', writer='Test Author', publisher='Test Publisher', shelf='Test Shelf', c_code=1920123456789)
        
        reserve = Reserve.objects.create(user_id=user, book_id=book, lending_start='2025-05-01', lending_end='2025-05-15')
        
        retrieved_reserve = Reserve.objects.first()
        self.assertEqual(retrieved_reserve, reserve)
        
    def test_saving_and_retrieving_Lending(self):
        user = User.objects.create(username='testuser', password='testpassword')
        library = Library.objects.create(ISBN=9784012345678, stock=1)
        book = Book.objects.create(ISBN=library, title='Test Book', writer='Test Author', publisher='Test Publisher', shelf='Test Shelf', c_code=1920123456789)
        
        lending = Lending.objects.create(user_id=user, book_id=book, lending_start='2025-05-01', lending_end='2025-05-15', returned=False)
        
        retrieved_lending = Lending.objects.first()
        self.assertEqual(retrieved_lending, lending)
        
    def test_saving_and_retrieving_News(self):
        news = News.objects.create(title='Test News', content='This is a test news content.')
        
        retrieved_news = News.objects.first()
        self.assertEqual(retrieved_news, news)
        
    def test_saving_and_retrieving_Contact(self):
        user = User.objects.create(username='testuser', password='testpassword')
        contact = Contact.objects.create(user_id=user, message='This is a test message.')
        
        retrieved_contact = Contact.objects.first()
        self.assertEqual(retrieved_contact, contact)
        
    def test_relation_book(self):
        library = Library.objects.create(ISBN=9784012345678, stock=1)
        book = Book.objects.create(ISBN=library, title='Test Book', writer='Test Author', publisher='Test Publisher', shelf='Test Shelf', c_code=1920123456789)
        
        self.assertEqual(book.ISBN, library)
    
    def test_relation_review(self):
        user = User.objects.create(username='testuser', password='testpassword')
        library = Library.objects.create(ISBN=9784012345678, stock=1)
        Book.objects.create(ISBN=library, title='Test Book', writer='Test Author', publisher='Test Publisher', shelf='Test Shelf', c_code=1920123456789)
        
        review = Review.objects.create(user_id=user, ISBN=library, stars=5, review='Great book!')
        
        self.assertEqual(review.user_id, user)
        self.assertEqual(review.ISBN, library)
        
    def test_relation_reserve(self):
        user = User.objects.create(username='testuser', password='testpassword')
        library = Library.objects.create(ISBN=9784012345678, stock=1)
        book = Book.objects.create(ISBN=library, title='Test Book', writer='Test Author', publisher='Test Publisher', shelf='Test Shelf', c_code=1920123456789)
        
        reserve = Reserve.objects.create(user_id=user, book_id=book, lending_start='2025-05-01', lending_end='2025-05-15')
        
        self.assertEqual(reserve.user_id, user)
        self.assertEqual(reserve.book_id, book)
        
    def test_relation_contact(self):
        user = User.objects.create(username='testuser', password='testpassword')
        contact = Contact.objects.create(user_id=user, message='This is a test message.')
        
        self.assertEqual(contact.user_id, user)
        
    def test_auto_now_add(self):
        user = User.objects.create(username='testuser', password='testpassword')
        
        review = Review.objects.create(user_id=user, ISBN=Library.objects.create(ISBN=9784012345678, stock=1), stars=5, review='Great book!')
        self.assertEqual(review.created_at, datetime.now().date())
        
        news = News.objects.create(title='Test News', content='This is a test news content.')
        self.assertEqual(news.created_at, datetime.now().date())
        
        contact = Contact.objects.create(user_id=user, message='This is a test message.')
        self.assertEqual(contact.created_at, datetime.now().date())
        
    def test_deletion(self):
        user = User.objects.create(username='testuser', password='testpassword')
        library = Library.objects.create(ISBN=9784012345678, stock=1)
        book = Book.objects.create(ISBN=library, title='Test Book', writer='Test Author', publisher='Test Publisher', shelf='Test Shelf', c_code=1920123456789)
        review = Review.objects.create(user_id=user, ISBN=library, stars=5, review='Great book!')
        reserve = Reserve.objects.create(user_id=user, book_id=book, lending_start='2025-05-01', lending_end='2025-05-15')
        lending = Lending.objects.create(user_id=user, book_id=book, lending_start='2025-05-01', lending_end='2025-05-15', returned=False)
        news = News.objects.create(title='Test News', content='This is a test news content.')
        contact = Contact.objects.create(user_id=user, message='This is a test message.')
        
        user_id = user.id
        library_id = library.ISBN
        book_id = book.id
        review_id = review.id
        reserve_id = reserve.id
        lending_id = lending.id
        news_id = news.id
        contact_id = contact.id
        
        review.delete()
        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(id=review_id)
            
        reserve.delete()
        with self.assertRaises(Reserve.DoesNotExist):
            Reserve.objects.get(id=reserve_id)
            
        lending.delete()
        with self.assertRaises(Lending.DoesNotExist):
            Lending.objects.get(id=lending_id)
            
        news.delete()
        with self.assertRaises(News.DoesNotExist):
            News.objects.get(id=news_id)
            
        contact.delete()
        with self.assertRaises(Contact.DoesNotExist):
            Contact.objects.get(id=contact_id)
            
        book.delete()
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=book_id)
            
        library.delete()
        with self.assertRaises(Library.DoesNotExist):
            Library.objects.get(ISBN=library_id)
            
        user.delete()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user_id)
            
    def test_str_method(self):
        user = User.objects.create(username='testuser', password='testpassword')
        library = Library.objects.create(ISBN=9784012345678, stock=1)
        book = Book.objects.create(ISBN=library, title='Test Book', writer='Test Author', publisher='Test Publisher', shelf='Test Shelf', c_code=1920123456789)
        review = Review.objects.create(user_id=user, ISBN=library, stars=5, review='Great book!')
        news = News.objects.create(title='Test News', content='This is a test news content.')
        contact = Contact.objects.create(user_id=user, message='This is a test message.')
        
        self.assertEqual(str(library), '9784012345678')
        self.assertEqual(str(book), 'Test Book')
        self.assertEqual(str(review), 'Test Book（testuser %s）' % str(datetime.now().date()))
        self.assertEqual(str(news), 'Test News')
        self.assertEqual(str(contact), 'testuserのメッセージ %s' % str(datetime.now().date()))