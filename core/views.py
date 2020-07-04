from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from.models import Question, Answer


class RecentQuestionView(ListView):
    model = Question
    context_object_name = "questions"
    template_name = "home.html"


class QuestionCreateView(CreateView):
    model = Question
    template_name = "question_add.html"


# class QuestionDetailView(DetailView):
#     model = Question
#     template_name = "question.html"
#     context_object_name = "question"

#     def get_context_data(self, **kwargs):
#         self.answers = get_object_or_404(Question, pk=self.kwargs.get('pk'))
#         extra_context = {
#             'answers': self.answers.answers.order_by('posted_on')
#         }
#         kwargs.update(extra_context)
#         return super().get_context_data(**kwargs)


class AnswerListView(ListView):
    model = Answer
    template_name = "question_answers.html"
    context_object_name = "answers"

    def get_context_data(self, session_key=None, **kwargs):

        session_key = 'viewed_question_{}'.format(self.question.pk)
        if not self.request.session.get(session_key, False):
            self.question.views += 1
            self.question.save()
            self.request.session[session_key] = True

        kwargs['question'] = self.question
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        queryset = self.question.answers.order_by('posted_on')
        return queryset
