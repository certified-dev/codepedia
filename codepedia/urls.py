from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from core import views

urlpatterns = [

    path('', views.HomeView.as_view(), name="home"),

    path('questions/', views.QuestionListView.as_view(), name="question"),

    path('question/<int:pk>-<slug:slug>/',
         views.AnswerListView.as_view(), name="question_detail"),

    path('question/ask/', views.QuestionCreateView.as_view(), name="ask_question"),

    path('question/<int:pk>-<slug:slug>/update/',
         views.QuestionUpdateView.as_view(), name="update_question"),

    path('question/<int:pk>/reply/',
         views.reply_question, name="reply_question"),

    path('question/answer/<int:pk>/reply/',
         views.reply_answer, name="reply_answer"),

    path('question/<int:pk>/answer/<int:answer_pk>/',
         views.AnswerUpdateView.as_view(), name="update_answer"),

    path('question/answer/<int:pk>/delete/',
         views.delete_answer, name="delete_answer"),

    path('question/<int:pk>/vote/',
         views.vote_question, name="vote_question"),

    path('answer/<int:pk>/vote/',
         views.vote_answer, name="vote_answer"),

    path('user/answers/',
         views.UserAnswersView.as_view(), name="user_answers"),

    path('user/questions/',
         views.UserQuestionsView.as_view(), name="user_questions"),

    path('users/',
         views.UsersListView.as_view(), name="users"),


    path('tags/', views.TagListView.as_view(), name="tags"),

    path('tagged/<int:pk>/questions/',
         views.TagQuestionView.as_view(), name="tag_question"),

    path('accounts/', include('allauth.urls')),


    path('admin/', admin.site.urls)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
