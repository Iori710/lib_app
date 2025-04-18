from django.test import TestCase
from django.contrib.auth.models import User
from ..forms import *
from ..models import *


class TestForms(TestCase):
    def test_lib_form(self):
        form = LibForm(data={"ISBN": "9784012345678"})
        self.assertTrue(form.is_valid())
            
    def test_book_register_form(self):
        form = BookRegisterForm(data={"shelf": "1F", "c_code": "1920123456789"})
        self.assertTrue(form.is_valid())
        
    def test_reserve_form(self):
        form = ReserveForm(data={"lending_start": "2025-04-17", "lending_end": "2025-04-17"})
        self.assertTrue(form.is_valid())
        
    def test_calendar_form(self):
        form = CalendarForm(data={"start_date": 20230101, "end_date": 20230110})
        self.assertTrue(form.is_valid())
        
    def test_review_form(self):
        form = ReviewForm(data={"stars": 5, "review": ""})
        self.assertTrue(form.is_valid())

        
    def test_user_form(self):
        user = User.objects.create(username="testuser")
        form = UserForm(data={"username": "newusername"}, instance=user)
        self.assertTrue(form.is_valid())
        
    def test_contact_form(self):
        form = ContactForm(data={"message": "This is a test message."})
        self.assertTrue(form.is_valid())