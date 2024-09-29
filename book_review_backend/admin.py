from django.contrib import admin
from .models import BookDetails, Review

# Register your models here.

admin.site.register(BookDetails)
admin.site.register(Review)