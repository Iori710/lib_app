from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Library(models.Model):
    ISBN = models.BigIntegerField(default=9784000000000,primary_key=True)
    stock = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.ISBN)
    
class Book(models.Model):
    ISBN = models.ForeignKey(Library,on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=100)
    writer = models.CharField('著者', max_length=50)
    publisher = models.CharField('出版社', max_length=50)
    shelf = models.CharField('保管場所', max_length=50)
    c_code = models.BigIntegerField('日本図書コード', default=1920000000000)
    
    def __str__(self):
        return self.title 
    
class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ISBN = models.ForeignKey(Library, on_delete=models.CASCADE)
    stars = models.IntegerField('評価(5段階)', default=1,validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user_id
    
class Reserve(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    lending_start = models.DateField("貸出日")
    lending_end = models.DateField("返却日")
    
class Lending(Reserve):
    returned = models.BooleanField(default=False)
    
class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Contact(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField("問い合わせ内容")
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user_id) + "のメッセージ " + str(self.created_at)
       