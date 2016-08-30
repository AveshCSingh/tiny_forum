from django.contrib.auth.models import User
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=80, unique=True)
    date = models.DateTimeField('date published', auto_now_add=True)


class Thread(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    date = models.DateTimeField('date published', auto_now_add=True)


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.CharField(max_length=10000)
    date = models.DateTimeField('date published', auto_now_add=True)
    user = models.ForeignKey('auth.User')


class Follow(models.Model):
    source = models.ForeignKey('auth.User', related_name='following')
    target = models.ForeignKey('auth.User', related_name='followed_by')
    created_at = models.DateTimeField('follow creation date', auto_now_add=True)

    class Meta:
        unique_together = ('source', 'target')
