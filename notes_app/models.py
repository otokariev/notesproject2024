from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=32, unique=True)
    text = models.TextField()

    def __str__(self):
        return self.title
