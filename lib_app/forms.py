from django import forms
from .models import Book

# Create your forms here.
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['ISBN', 'shelf', 'c_code']