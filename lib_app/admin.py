from django.contrib import admin
from .models import Book, Reserve, Lending

# Register your models here.
admin.site.register(Book)
admin.site.register(Reserve)
admin.site.register(Lending)