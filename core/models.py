from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=5000)
    tags = models.ManyToManyField(Tag)
    points = models.IntegerField(default=0)
    asked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers")
    text = models.TextField(max_length=5000)
    points = models.IntegerField(default=0)
    answered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.CharField(max_length=5000)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class User(AbstractUser):
    upvoted_questions = models.ManyToManyField(
        Question, related_name="upvoted_users")
    downvoted_questions = models.ManyToManyField(
        Question, related_name="downvoted_users")
    upvoted_answers = models.ManyToManyField(
        Answer, related_name="upvoted_users")
    downvoted_answers = models.ManyToManyField(
        Answer, related_name="downvoted_users")
    reputation = models.PositiveIntegerField(default=0)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username
