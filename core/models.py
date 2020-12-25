from hashlib import md5
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.html import urlize
from markdown2 import Markdown
from rest_framework import serializers

markdowner = Markdown(html4tags=True)


def update_score(obj):
    upvotes = obj.upvoted_users.filter(
        banned=False).distinct().count()
    downvotes = obj.downvoted_users.filter(
        banned=False).distinct().count()
    obj.score = upvotes - downvotes
    obj.save()


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Comment(models.Model):
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    text = models.CharField(max_length=5000)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text


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
    slug = models.SlugField(max_length=1000)
    comments = GenericRelation(Comment, related_query_name="question_comments")

    def show_points(self):
        if self.points < 0:
            return 0
        else:
            return self.points

    def update_points(self):
        update_score(self)

    def any_answer_accepted(self):
        answer_accepted = False
        if self.answers.filter(accepted=True).exists():
            answer_accepted = True
        return answer_accepted

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
    comments = GenericRelation(Comment, related_query_name="answer_comments")

    def __str__(self):
        return self.body

    def update_points(self):
        update_score(self)

    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"pk": self.question.pk, 'slug': self.question.slug})


class User(AbstractUser):
    upvoted_questions = models.ManyToManyField(
        Question, related_name="upvoted_users", blank=True)
    downvoted_questions = models.ManyToManyField(
        Question, related_name="downvoted_users", blank=True)
    upvoted_answers = models.ManyToManyField(
        Answer, related_name="upvoted_users", blank=True)
    downvoted_answers = models.ManyToManyField(
        Answer, related_name="downvoted_users", blank=True)
    points = models.IntegerField(default=1)
    banned = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank="True")
    title = models.CharField(max_length=100, blank="True")
    display_photo = models.ImageField(upload_to='users', blank=True)
    description = models.TextField(max_length=1000, blank=True)
    watched = models.ManyToManyField(Tag, related_name="watched_tags", blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("user", kwargs={"pk": self.pk})

    def question_once_upvote_now_downvote(self):
        if self.points > 1:
            self.points -= 12
            self.save()
        else:
            pass

    def question_once_downvote_now_upvote(self):
        if self.points < 2:
            self.points += 10
            self.save()
        else:
            self.points += 12
            self.save()

    def question_vote_up(self):
        self.points += 10
        self.save()

    def question_vote_down(self):
        if self.points > 1:
            self.points -= 2
            self.save()
        else:
            pass

    def question_cancel_upvote(self):
        if self.points > 1:
            self.points -= 10
            self.save()
        else:
            pass

    def question_cancel_downvote(self):
        self.points += 2
        self.save()

    def answer_vote_down(self):
        if self.points > 1:
            self.points -= 2
            self.save()
        else:
            pass

    def answer_vote_up(self):
        self.points += 10
        self.save()

    def answer_cancel_upvote(self):
        if self.points > 1:
            self.points -= 10
            self.save()
        else:
            pass

    def answer_cancel_downvote(self):
        self.points += 2
        self.save()

    def answer_once_upvote_now_downvote(self):
        if self.points > 1:
            self.points -= 12
            self.save()
        else:
            pass

    def answer_once_downvote_now_upvote(self):
        if self.points < 2:
            self.points += 10
            self.save()
        else:
            self.points += 12
            self.save()

    def accepted_answer(self):
        self.points += 15
        self.save()

    def accepted_answer_cancel(self):
        if self.points > 1:
            self.points -= 15
            self.save()
        else:
            pass


class UserField(serializers.Field):
    def to_representation(self, value):
        return value.username


class CommentSerializer(serializers.ModelSerializer):
    text_html = serializers.SerializerMethodField()
    posted_on = serializers.SerializerMethodField()
    posted_by_id = serializers.SerializerMethodField()
    posted_by = UserField()

    class Meta:
        model = Comment
        fields = ('id', 'text_html', 'posted_by', 'posted_by_id', 'posted_on')

    def get_text_html(self, obj):
        return urlize(obj.text)

    def get_posted_on(self, obj):
        return naturaltime(obj.posted_on)

    def get_posted_by_id(self, obj):
        return obj.posted_by.id


class AnswerSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    answered_by = UserField()
    question_owner = serializers.SerializerMethodField()
    text_html = serializers.SerializerMethodField()
    posted_on = serializers.SerializerMethodField()
    updated_on = serializers.SerializerMethodField()
    answered_by_points = serializers.SerializerMethodField()
    answered_by_id = serializers.SerializerMethodField()
    answered_by_image = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ('question_owner', 'text_html', 'score', 'answered_by', 'pk', 'answered_by_points', 'answered_by_id',
                  'posted_on', 'accepted', 'updated_on', 'comments', 'answered_by_image')

    @staticmethod
    def get_question_owner(obj):
        return obj.question.asked_by.username

    @staticmethod
    def get_text_html(obj):
        return markdowner.convert(obj.body)

    @staticmethod
    def get_posted_on(obj):
        return naturaltime(obj.posted_on)

    @staticmethod
    def get_updated_on(obj):
        return naturaltime(obj.updated_on)

    @staticmethod
    def get_answered_by_points(obj):
        return obj.answered_by.points
        

    @staticmethod
    def get_answered_by_id(obj):
        return obj.answered_by.id

    @staticmethod
    def get_answered_by_image(obj):
        if obj.answered_by.display_photo:
            return obj.answered_by.display_photo.url
        else:
            email_hash = md5(
                str(obj.answered_by.email.strip().lower()).encode()).hexdigest()
            avatar_url = "https://www.gravatar.com/avatar/%s" % email_hash + "?s=28&d=identicon&r=PG"
            return avatar_url
