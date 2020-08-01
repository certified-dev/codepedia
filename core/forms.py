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


class NewPageDownWidget(PagedownWidget):
    class Media:
        css = {
            'all': ('pagedown/pagedown.css',)
        }


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
            'title': forms.TextInput(attrs={'placeholder': 'Be specific and imagine you’re asking a question to another person'}),
            'body': NewPageDownWidget(attrs={'rows': 8, 'placeholder': 'include all the information someone would need to answer your question'}),
            "tags": TagsWidget(attrs={'data-width': '100%', 'data-placeholder': 'Add up to 5 tags to describe what your question is about'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control-sm'})
        self.fields['body'].widget.attrs.update(
            {'class': 'wmd-input pagedownwidget form-control form-control-sm'})
        self.fields['tags'].widget.attrs.update({'class': 'form-control-sm'})


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('body',)
        widgets = {
            'body': NewPageDownWidget(attrs={'rows': 8, 'placeholder': 'make your answer as clear as possible,easy to understand'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update(
            {'class': 'wmd-input pagedownwidget form-control form-control-sm'})


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class UserUpdateForm(forms.ModelForm):
    pass
