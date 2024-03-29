from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from django.forms.fields import CharField
from django_select2 import forms as s2forms
from pagedown.widgets import PagedownWidget

from .models import Answer, Comment, Question, Tag

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

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        print("saved")
        return user


class AddWatchedForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('watched',)
        widgets = {
            "watched": TagsWidget(attrs={'data-width': '100%',
                                         'data-placeholder': 'enter at least one technology/terminology to watch for.'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['watched'].widget.attrs.update({'class': 'form-control-sm'})


class AddWatched(forms.ModelForm):
    watched = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    class Meta:
        model = User
        fields = ('watched',)
        

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'title', 'location', 'description', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Doe'}),
            'title': forms.TextInput(attrs={'placeholder': 'No title has been set'}),
            'email': forms.TextInput(attrs={'placeholder': 'No email has been added'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter a location'}),
            'description': NewPageDownWidget(attrs={'rows': 8, 'placeholder': 'Say something about yourself...'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control form-control-sm'})
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control form-control-sm'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control form-control-sm'})
        self.fields['location'].widget.attrs.update(
            {'class': 'form-control form-control-sm'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control form-control-sm'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control form-control-sm'})
        self.fields['description'].widget.attrs.update(
            {'class': 'wmd-input pagedownwidget form-control form-control-sm'})


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'body', 'tags')
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Be specific and imagine you’re asking a question to another person.'}),
            'body': NewPageDownWidget(attrs={'rows': 8,
                                             'placeholder': 'include all the information someone would need to answer '
                                                            'your question.'}),
            "tags": TagsWidget(attrs={'data-width': '100%',
                                      'data-placeholder': 'Add up to 5 tags to describe what your question is about.'})
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
            'body': NewPageDownWidget(
                attrs={'rows': 8, 'placeholder': 'make your answer as clear as possible,easy to understand.'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update(
            {'class': 'wmd-input pagedownwidget form-control form-control-sm'})


class UploadPhotoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('display_photo',)
