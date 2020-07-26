from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Answer, Question, Tag, Comment, Question
from django_select2 import forms as s2forms
from pagedown.widgets import PagedownWidget

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
    # body = forms.CharField(widget=PagedownWidget())
    class Meta:
        model = Question
        fields = ('title', 'body', 'tags')
        widgets = {
            'title' : forms.TextInput(attrs={'placeholder': 'Be specific and imagine you’re asking a question to another person'}),
            'body'  : PagedownWidget(attrs={'rows': 6,'placeholder': 'include all the information someone would need to answer your question'}),
            "tags": TagsWidget(attrs={'data-width' : '100%','data-placeholder' : 'Add up to 5 tags to describe what your question is about'})
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('body',)
        widgets = {
            'body'  : PagedownWidget(attrs={'rows': 5,'placeholder': 'make your answer as clear as possible,easy to understand'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)