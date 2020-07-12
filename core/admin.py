from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Question, Answer, Tag, Comment


admin.site.register(User)

admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Comment)

admin.site.unregister(Group)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
