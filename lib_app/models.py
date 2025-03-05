from django.db import models
from datetime import date, timedelta

# Create your models here.
class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    email = models.EmailField
    HN = models.CharField(max_length=50)
    PW = models.CharField(max_length=50)

    
class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    ISBN = models.BigIntegerField(default=3784000000000)
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    shelf = models.CharField(max_length=50)
    c_code = models.BigIntegerField(default=1920000000000)
    
class Library(models.Model):
    ISBN = models.ForeignKey(Book,on_delete=models.CASCADE,primary_key=True)
    stock = models.IntegerField(default=1)
    
class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ISBN = models.ForeignKey(Library, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    review = models.TextField(blank=True)
    
class Reserve(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    lending_start = models.DateField(default=date.today())
    lending_end = models.DateField(default=date.today() + timedelta(days=7))
    
class Lending(Reserve):
    returned = models.BooleanField(default=False)
    
    
    