from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    email = models.EmailField
    HN = models.CharField(max_length=50)
    PW = models.CharField(max_length=50)
    
class Library(models.Model):
    ISBN = models.BigIntegerField(primary_key=True)
    stock = models.IntegerField
    
class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    ISBN = models.ForeignKey(Library, on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    shelf = models.CharField(max_length=50)
    num_of_books = models.IntegerField
    c_code = models.BigIntegerField
    
class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    