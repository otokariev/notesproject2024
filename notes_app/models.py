from django.contrib.auth.models import User
from django.db import models


class NoteCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    category = models.ForeignKey(NoteCategory, on_delete=models.SET_NULL, null=True, blank=True)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.search_text = self.title.lower()
        super().save(*args, **kwargs)
