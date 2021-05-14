from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core import views

urlpatterns = [
                  path("update_server/", views.update, name="update"),

                  path('notifications/', include('notify.urls', 'notifications')),

                  path('', include('pagedown.urls')),

                  path('admin/', admin.site.urls),

                  path('accounts/', include('allauth.urls')),


                  path("select2/", include("django_select2.urls")),

                  path('ajax/validate_username/', views.check_user, name="check_user"),

                  path('', views.home, name="home"),

                  path('home/', views.HomeQuestionView.as_view(), name="home_question"),

                  path('questions/', views.QuestionListView.as_view(), name="question"),

                  path('questions/unanswered/', views.UnansweredQuestion.as_view(), name="unanswered"),

                  path('question/<int:pk>/<slug:slug>/',
                       views.AnswerListView.as_view(), name="question_detail"),

                  # add question
                  path('question/ask/', views.QuestionCreateView.as_view(), name="ask_question"),

                  # update question
                  path('question/<int:pk>/<slug:slug>/update/',
                       views.QuestionUpdateView.as_view(), name="update_question"),

                  # add comment to an question
                  path('question/<int:pk>/reply/comment/',
                       views.comment_question_ajax, name="comment_question"),

                  # add answer to a question
                  path('question/<int:pk>/<slug:slug>/reply/answer/',
                       views.reply_question, name="reply_question"),

                  # add comment to an answer
                  path('answer/<int:pk>/reply/',
                       views.reply_answer_ajax, name="reply_answer"),

                  # update answer
                  path('question/<int:pk>/answer/<int:answer_pk>/update/',
                       views.AnswerUpdateView.as_view(), name="update_answer"),

                  path('question/<int:pk>/<slug:slug>/vote/',
                       views.vote_question, name="vote_question"),

                  path('answer/<int:pk>/vote/',
                       views.vote_answer, name="vote_answer"),

                  path('users/',
                       views.UsersListView.as_view(), name="users"),

                  path('users/<int:pk>/<str:username>/',
                       views.UserDetailView.as_view(), name="user"),

                  path('user/<int:pk>/update/',
                       views.UserUpdateView.as_view(), name="user_update"),

                  path('user/photo/upload/',
                       views.upload_photo, name="upload_photo"),

                  path('tags/', views.TagListView.as_view(), name="tags"),

                  path('tagged/<int:pk>/<str:tag>/questions/',
                       views.TagQuestionView.as_view(), name="tag_question"),

                  path('user/<int:pk>/watched/update/', views.TagUpdateView.as_view(), name="tag_edit"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
