from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Question, Answer, Tag, User, AnswerSerializer
from .forms import AnswerForm, CommentForm, QuestionForm


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
    form_class = QuestionForm
    template_name = "question_add.html"

    def form_valid(self, form):
        self.question = form.save(commit=False)
        self.question.asked_by = self.request.user
        self.question.slug = slugify(form.cleaned_data['title'])
        self.question.save()
        return super(QuestionCreateView, self).form_valid(form)


@method_decorator([login_required], name="dispatch")
class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "question_update.html"
    context_object_name = 'question'

    def form_valid(self, form):
        self.question = form.save(commit=False)
        self.question.updated_on = timezone.now()
        self.question.slug = slugify(form.cleaned_data['title'])
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

        # question
        upvoted = False
        downvoted = False

        if not self.request.user.is_authenticated:
            pass
        elif self.request.user.upvoted_questions.filter(pk=self.question.pk).exists():
            upvoted = True
        elif self.request.user.downvoted_questions.filter(pk=self.question.pk).exists():
            downvoted = True

        # answers
        answers = self.question.answers.exclude(
            hidden=True).order_by('posted_on')
        answers_serialized = AnswerSerializer(answers, many=True).data
        for answer in answers_serialized:
            answer['upvoted'] = False
            answer['downvoted'] = False

            if not self.request.user.is_authenticated:
                pass
            elif self.request.user.upvoted_answers.filter(pk=answer['pk']).exists():
                answer['upvoted'] = True
            elif self.request.user.downvoted_answers.filter(pk=answer['pk']).exists():
                answer['downvoted'] = True

        extra_context = {
            'form': AnswerForm(),
            'question': self.question,
            'points': self.question.points,
            'user_answers': user_answers,
            'upvoted': upvoted,
            'downvoted': downvoted,
            'answers_serialized': answers_serialized
        }
        kwargs.update(extra_context)
        return super(AnswerListView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        queryset = self.question.answers.order_by('posted_on')
        return queryset


@login_required
def reply_question(request, pk, slug):
    question = get_object_or_404(Question, pk=pk, slug=slug)
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
    form_class = AnswerForm
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


class UsersListView(ListView):
    model = User
    template_name = "users.html"
    context_object_name = 'users'

    def get_queryset(self):
        queryset = User.objects.exclude(
            id=self.request.user.id).order_by('-points')
        return queryset


class UserDetailView(DetailView):
    model = User
    template_name = "user.html"
    context_object_name = 'user_detail'

    def get_context_data(self, *args, **kwargs):
        user_questions = Question.objects.filter(
            asked_by_id=self.kwargs.get('pk')).order_by('-posted_on')
        user_answers = Answer.objects.filter(
            answered_by_id=self.kwargs.get('pk')).order_by('-posted_on')

        user = User.objects.get(pk=self.kwargs.get('pk'))

        upvoted_answers = user.upvoted_answers.count()
        downvoted_answers = user.downvoted_answers.count()
        upvoted_questions = user.upvoted_questions.count()
        downvoted_questions = user.downvoted_questions .count()

        extra_context = {
            'user_questions': user_questions,
            'user_answers': user_answers,
            'all_posts':  user_answers.count() + user_questions.count(),
            'votes': upvoted_answers + downvoted_answers + upvoted_questions + downvoted_questions
        }
        kwargs.update(extra_context)
        return super(UserDetailView, self).get_context_data(**kwargs)


@method_decorator([login_required], name="dispatch")
class ProfileView(DetailView):
    model = User
    template_name = "user.html"
    context_object_name = 'user_detail'

    def get_context_data(self, *args, **kwargs):
        user_questions = Question.objects.filter(
            asked_by=self.request.user).order_by('-posted_on')
        user_answers = Answer.objects.filter(
            answered_by=self.request.user).order_by('-posted_on')

        upvoted_answers = self.request.user.upvoted_answers.count()
        downvoted_answers = self.request.user.downvoted_answers.count()
        upvoted_questions = self.request.user.upvoted_questions.count()
        downvoted_questions = self.request.user.downvoted_questions .count()

        extra_context = {
            'user_questions': user_questions,
            'user_answers': user_answers,
            'all_posts': user_answers.count() + user_questions.count(),
            'votes': upvoted_answers + downvoted_answers + upvoted_questions + downvoted_questions
        }
        kwargs.update(extra_context)
        return super(ProfileView, self).get_context_data(**kwargs)


def vote_question(request, pk, slug):
    return vote(request, pk, 'question')


def vote_answer(request, pk):
    return vote(request, pk, 'answer')


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


def vote(request, pk, question_or_answer):

    if not request.user.is_authenticated:
        return HttpResponse('Not logged in', status=401)

    if question_or_answer == 'question':
        target = Question.objects.get(pk=pk)
        if request.user.id == target.asked_by_id:
            return HttpResponseBadRequest('Same user')
    else:
        target = Answer.objects.get(pk=pk)
        if request.user.id == target.answered_by_id:
            return HttpResponseBadRequest('Same user')

    if request.method == 'POST':
        vote_type = request.POST.get('vote_type')
        points = update_vote(request.user, target,
                             vote_type, question_or_answer)

        if question_or_answer == 'answer':
            target.answered_by.update_points()

        # if question_or_answer == "question":
        #     target.asked_by.update_test_points()

        return JsonResponse({'vote_type': vote_type, 'points': points})

    else:
        return HttpResponseBadRequest('The request is not POST')
