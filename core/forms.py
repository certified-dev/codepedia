from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Answer, Question, Tag, Comment, Question
from django_select2 import forms as s2forms

User = get_user_model()


class TagsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
    ]


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Enter email address'}), required=True)

    class Meta(UserCreationForm.Meta):
        model = User


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'body', 'tags')
        widgets = {
            "tags": TagsWidget
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
