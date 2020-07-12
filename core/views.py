from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Question, Answer, Tag, User
from .forms import AnswerForm, CommentForm


class HomeView(ListView):
    model = Question
    context_object_name = "questions"
    template_name = "home.html"

    def get_queryset(self):
        queryset = super(HomeView, self).get_queryset()
        queryset = Question.objects.filter(hidden=False).order_by('-pk')[:15]
        return queryset


class QuestionListView(ListView):
    model = Question
    context_object_name = "questions"
    template_name = "question.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super(QuestionListView, self).get_queryset()
        queryset = Question.objects.filter(hidden=False).order_by('-posted_on')
        return queryset


@method_decorator([login_required], name="dispatch")
class QuestionCreateView(CreateView):
    model = Question
    fields = ('title', 'body', 'tags')
    template_name = "question_add.html"

    def form_valid(self, form):
        self.question = form.save(commit=False)
        self.question.asked_by = self.request.user
        self.question.save()
        return super(QuestionCreateView, self).form_valid(form)


@method_decorator([login_required], name="dispatch")
class QuestionUpdateView(UpdateView):
    model = Question
    fields = ('title', 'body', 'tags')
    template_name = "question_update.html"
    context_object_name = 'question'

    def form_valid(self, form):
        self.question = form.save(commit=False)
        self.question.updated_on = timezone.now()
        self.question.save()
        return super(QuestionUpdateView, self).form_valid(form)


class AnswerListView(ListView):
    model = Answer
    template_name = "question_answers.html"
    context_object_name = "answers"
    paginate_by = 10

    def get_context_data(self, session_key=None, **kwargs):

        session_key = 'viewed_question_{}'.format(self.question.pk)
        if not self.request.session.get(session_key, False):
            self.question.views += 1
            self.question.save()
            self.request.session[session_key] = True

        user_answers = None
        if self.request.user.is_authenticated:
            user_answers = self.question.answers.filter(
                answered_by=self.request.user)

        upvoted = False
        downvoted = False

        if not self.request.user.is_authenticated:
            pass
        elif self.request.user.upvoted_questions.filter(pk=self.question.pk).count() > 0:
            upvoted = True
        elif self.request.user.downvoted_questions.filter(pk=self.question.pk).count() > 0:
            downvoted = True

        extra_context = {
            'question': self.question,
            'user_answers': user_answers,
            'upvoted': upvoted,
            'downvoted': downvoted
        }
        kwargs.update(extra_context)
        return super(AnswerListView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        queryset = self.question.answers.order_by('posted_on')
        return queryset


@login_required
def reply_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.answered_by = request.user
            answer.save()
            return redirect(question)


@method_decorator([login_required], name="dispatch")
class AnswerUpdateView(UpdateView):
    model = Answer
    fields = ('text',)
    template_name = "answer_update.html"
    pk_url_kwarg = 'answer_pk'
    context_object_name = 'answer'

    def form_valid(self, form):
        self.answer = form.save(commit=False)
        self.answer.updated_on = timezone.now()
        self.answer.save()
        return super().form_valid(form)

    def get_success_url(self):
        answer = self.get_object()
        return reverse('question_detail', kwargs={'pk': answer.question.pk, 'slug': answer.question.slug})


@login_required
def delete_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if request.method == 'POST':
        answer.delete()
        return redirect(answer.question)


@login_required
def reply_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.answer = answer
            comment.posted_by = request.user
            comment.save()
            return redirect(answer.question)


class TagListView(ListView):
    model = Tag
    template_name = "tag_list.html"
    context_object_name = 'tags'
    paginate_by = 10


class TagQuestionView(DetailView):
    model = Tag
    template_name = "tag_details.html"
    context_object_name = 'tag'


class UserQuestionsView(ListView):
    model = Question
    template_name = "questions.html"
    context_object_name = 'questions'
    paginate_by = 10

    def get_queryset(self):
        queryset = Question.objects.filter(
            asked_by=self.request.user, hidden=False).order_by('posted_on')
        return queryset


class UserAnswersView(ListView):
    model = Answer
    template_name = "answers.html"
    context_object_name = 'answers'
    paginate_by = 10

    def get_queryset(self):
        queryset = Answer.objects.filter(
            answered_by=self.request.user).order_by('posted_on')
        return queryset


class UsersListView(ListView):
    model = User
    template_name = "users.html"
    context_object_name = 'users'

    def get_queryset(self):
        queryset = User.objects.exclude(
            id=self.request.user.id).order_by('-points')
        return queryset


def vote_question(request, pk):
    return vote(request, pk, 'answer')


def vote_answer(request, pk):
    return vote(request, pk, 'question')


def update_vote(user, target, vote_type, question_or_answer):
    if question_or_answer == 'question':
        upvoted_targets = user.upvoted_questions
        downvoted_targets = user.downvoted_questions
    else:
        upvoted_targets = user.upvoted_answers
        downvoted_targets = user.downvoted_answers

    upvoted_targets.remove(target)
    downvoted_targets.remove(target)

    # if this is an upvote, add an upvote. otherwise, add a downvote.
    if vote_type == 'upvote':
        upvoted_targets.add(target)
    elif vote_type == 'downvote':
        downvoted_targets.add(target)

    target.update_points()
    return target.points

# def vote(request, pk, questio_or_answer):
#     if question_or_answer == 'question':
#         target = Question.objects.get(pk=pk)
#     else:
#         target = Answer.objects.get(pk=pk)
