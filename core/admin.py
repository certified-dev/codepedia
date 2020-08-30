from pagedown.widgets import AdminPagedownWidget
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db import models
from .models import User, Question, Answer, Tag, Comment, Question_Comment


admin.site.register(User)

admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Question_Comment)

admin.site.unregister(Group)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
