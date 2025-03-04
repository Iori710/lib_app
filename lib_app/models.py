from django.db import models

# Create your models here.
class user(models.Model):
    user_id = models.IntegerField
    email = models.EmailField
    HN = models.CharField(max_length=50)
    PW = models.CharField(max_length=50)
    
class library(models.Model):
    book_id = models.IntegerField
    ISBN = models.BigIntegerField
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    shelf = models.CharField(max_length=50)
    num_of_books = models.IntegerField
    c_code = models.BigIntegerField