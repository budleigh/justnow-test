from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Count
from random import randint


class Entry(models.Model):
    user = models.ForeignKey(User, related_name='entries', on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField(db_index=True)


class QuestionManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class Question(models.Model):
    entry = models.ForeignKey(Entry, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    objects = QuestionManager()


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    private = models.BooleanField()


class Message(models.Model):
    user_from = models.ForeignKey(User, related_name='sent_messages', on_delete=models.DO_NOTHING)
    user_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.DO_NOTHING)
