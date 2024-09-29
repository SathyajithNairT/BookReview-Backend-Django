from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    

class BookDetails(models.Model):
    title = models.CharField(max_length = 1000)
    author = models.CharField(max_length = 500)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    userID = models.ForeignKey(User, on_delete= models.CASCADE)
    bookID = models.ForeignKey(BookDetails, on_delete= models.CASCADE)
    review = models.TextField()

    def __str__(self):
        return self.review

