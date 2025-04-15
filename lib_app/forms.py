from django import forms
from .models import Library, Book, Review, Reserve, Contact
from django.contrib.auth.models import User

class LibForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['ISBN']
        
class BookRegisterForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['shelf', 'c_code']
        
class ReserveForm(forms.ModelForm):
    class Meta:
        model = Reserve
        fields = ['lending_start', 'lending_end']

class CalendarForm(forms.Form):
    start_date = forms.IntegerField(required=True)
    end_date = forms.IntegerField(required=True)
    
class ReviewForm(forms.Form):
    STAR_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    stars = forms.ChoiceField(choices=STAR_CHOICES, widget=forms.Select, label="評価(5段階)")
    review = forms.CharField(widget=forms.Textarea, label="レビュー", required=False)
        
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

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['message']
