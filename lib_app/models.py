from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

# Create your models here.

class Library(models.Model):
    ISBN = models.BigIntegerField(default=9784000000000,primary_key=True)
    stock = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.ISBN)
    
class Book(models.Model):
    ISBN = models.ForeignKey(Library,on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=100)
    writer = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    shelf = models.CharField('保管場所', max_length=50)
    c_code = models.BigIntegerField('日本図書コード', default=1920000000000)
    
    def __str__(self):
        return self.title 
    
class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ISBN = models.ForeignKey(Library, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    review = models.TextField(null=True)
    
class Reserve(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    lending_start = models.DateField(default=date.today())
    lending_end = models.DateField(default=date.today() + timedelta(days=7))
    
class Lending(Reserve):
    returned = models.BooleanField(default=False)
    
    
    