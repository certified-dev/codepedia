from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Answer, Question, Tag, Comment, Question

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Enter email address'}), required=True)

    class Meta(UserCreationForm.Meta):
        model = User


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'body', 'tags')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
