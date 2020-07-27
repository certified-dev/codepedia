from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe, urlize, escape
from functools import reduce
from django.db.models import Q
from rest_framework import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime
from markdown2 import Markdown

markdowner = Markdown(html4tags=True)


def update_points_helper(obj):
    upvotes = obj.upvoted_users.filter(
        banned=False).distinct().count()
    downvotes = obj.downvoted_users.filter(
        banned=False).distinct().count()
    downvotes += obj.downvoted_users.filter(is_staff=True).count()
    obj.score = upvotes - downvotes
    obj.save()


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=1000)
    body = models.TextField(max_length=10000)
    tags = models.ManyToManyField(Tag, related_name="question_tags")
    score = models.IntegerField(default=0)
    asked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True, blank=True)
    hidden = models.BooleanField(default=False)
    slug = models.SlugField(max_length=1000, null=True)

    def show_points(self):
        if self.points < 0:
            return 0
        else:
            return self.points

    def update_points(self):
        update_points_helper(self)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"pk": self.pk, 'slug': self.slug})


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers")
    body = models.TextField(max_length=10000)
    score = models.IntegerField(default=0)
    answered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    accepted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    def update_points(self):
        update_points_helper(self)

    def __str__(self):
        return self.body


class Comment(models.Model):
    text = models.CharField(max_length=5000)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name="comments")

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
    points = models.IntegerField(default=1)
    adjustment_points = models.IntegerField(default=0)
    banned = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    # def update_points(self):
    #     answers = self.answer_set.filter(~Q(points=0))
    #     points = map(lambda a: a.points, answers)
    #     user_points = reduce(lambda x, y: x + y, points, 0)
    #     self.points = user_points + self.adjustment_points
    #     self.save()
    def question_once_upvote_now_downvote(self):
        self.points -= 12
        self.save()

    def question_once_downvote_now_upvote(self):
        self.points += 12
        self.save()

    def question_vote_up(self):
        self.points += 10
        self.save()

    def question_vote_down(self):
        self.points -= 2
        self.save()

    def question_cancel_upvote(self):
        self.points -= 10
        self.save()

    def question_cancel_downvote(self):
        self.points += 2
        self.save()

    def answer_vote_down(self):
        self.points -= 2
        self.save()

    def answer_vote_up(self):
        self.points += 10
        self.save()

    def answer_cancel_upvote(self):
        self.points -= 10
        self.save()

    def answer_cancel_downvote(self):
        self.points += 2
        self.save()

    def answer_once_upvote_now_downvote(self):
        self.points -= 12
        self.save()

    def answer_once_downvote_now_upvote(self):
        self.points += 12
        self.save()

    def accepted_answer(self):
        self.points += 15
        self.save()

    def accepted_answer_cancel(self):
        self.points -= 15
        self.save()


class UserField(serializers.Field):
    def to_representation(self, value):
        return value.username


class AnswerSerializer(serializers.ModelSerializer):
    answered_by = UserField()
    text_html = serializers.SerializerMethodField()
    posted_on = serializers.SerializerMethodField()
    updated_on = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ('text_html', 'score', 'answered_by', 'pk',
                  'posted_on', 'accepted', 'updated_on')

    def get_text_html(self, obj):
        return markdowner.convert(obj.body)

    def get_posted_on(self, obj):
        return naturaltime(obj.posted_on)

    def get_updated_on(self, obj):
        return naturaltime(obj.posted_on)
