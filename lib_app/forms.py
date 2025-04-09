from django import forms
from .models import Library, Book, Review, Reserve
from django.contrib.auth.models import User

class LibForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['ISBN']
        
class BookRegisterForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['shelf', 'c_code']
        
class BookSearchForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'writer', 'publisher']
        
class ReserveForm(forms.ModelForm):
    class Meta:
        model = Reserve
        fields = ['lending_start', 'lending_end']

class CalendarForm(forms.Form):
    start_date = forms.IntegerField(required=True)
    end_date = forms.IntegerField(required=True)
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['stars', 'review']
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '新しいユーザーネーム'}),
        }
        labels = {
            'username': '新しいユーザーネーム',
        }