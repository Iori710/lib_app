from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    email = models.EmailField
    HN = models.CharField(max_length=50)
    PW = models.CharField(max_length=50)

    
class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    ISBN = models.BigIntegerField
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    shelf = models.CharField(max_length=50)
    num_of_books = models.IntegerField
    c_code = models.BigIntegerField
    
class Library(models.Model):
    ISBN = models.ForeignKey(Book,on_delete=models.CASCADE,primary_key=True)
    stock = models.IntegerField
    
class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ISBN = models.ForeignKey(Library, on_delete=models.CASCADE)
    stars = models.IntegerField
    review = models.TextField(blank=True)
    
class Reserve(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    lending_start = models.DateField
    lending_end = models.DateField
    
class Lending(Reserve):
    returned = models.BooleanField(default=False)
    
    
    