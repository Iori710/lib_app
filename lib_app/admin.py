from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Book)
admin.site.register(models.Library)
admin.site.register(models.Reserve)
admin.site.register(models.Lending)
admin.site.register(models.Review)
admin.site.register(models.News)
admin.site.register(models.Contact)
