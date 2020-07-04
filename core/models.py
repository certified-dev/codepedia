from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    points = models.PositiveIntegerField(default=0)
    reputation = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=5000)
    tags = models.ManyToManyField(Tag)
    asked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name="answers")
    text = models.CharField(max_length=5000)
    answered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.CharField(max_length=5000)
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text


