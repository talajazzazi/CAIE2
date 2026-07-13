from django.contrib.auth.models import User
from django.db import models

class Post (models.Model):
    title_id = models.BigAutoField(primary_key=True)
    title = models.CharField( max_length=100)
    content = models.TextField(max_length=500)
    date = models.DateField()