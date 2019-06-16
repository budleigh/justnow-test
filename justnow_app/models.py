from django.db import models
from django.contrib.auth.models import User


class Entry(models.Model):
    user = models.ForeignKey(User, related_name='entries', on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField(db_index=True)


class Question(models.Model):
    entry = models.ForeignKey(Entry, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()


class Answer(models.Model):
    entry = models.ForeignKey(Entry, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
