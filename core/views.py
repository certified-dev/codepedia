
from itertools import chain
import git
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Question, Answer, Tag, User, AnswerSerializer
from .forms import AnswerForm, CommentForm, QuestionForm, UserUpdateForm


@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be 
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo("Karma.pythonanywhere.com/")
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect('home_question')


class HomeQuestionView(ListView):
    model = Question
    context_object_name = "questions"
    template_name = "home_question.html"

    # filter according to user tag watch
    def get_queryset(self):
        queryset = super(HomeQuestionView, self).get_queryset()
        queryset = Question.objects.filter(hidden=False).order_by('-pk')[:20]
        return queryset


class QuestionListView(ListView):
    model = Question
    context_object_name = "questions"
    template_name = "question.html"
    paginate_by = 15

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
    template_name = "question_add.html"
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
    paginate_by = 16
    ordering = ('id')


class TagQuestionView(DetailView):
    model = Tag
    template_name = "tag_details.html"
    context_object_name = 'tag'


class UsersListView(ListView):
    model = User
    template_name = "users.html"
    context_object_name = 'users'
    paginate_by = 20
    ordering = ('-points')


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
        all_posts = list(chain(user_answers, user_questions))

        for post in user_answers:
            post.is_answer = True

        for post in user_questions:
            post.is_question = True

        upvoted_answers = user.upvoted_answers.count()
        downvoted_answers = user.downvoted_answers.count()
        upvoted_questions = user.upvoted_questions.count()
        downvoted_questions = user.downvoted_questions .count()

        extra_context = {
            'user_questions': user_questions,
            'user_answers': user_answers,
            'all_posts':  all_posts,
            'all_posts_count':  user_answers.count() + user_questions.count(),
            'votes': upvoted_answers + downvoted_answers + upvoted_questions + downvoted_questions
        }
        kwargs.update(extra_context)
        return super(UserDetailView, self).get_context_data(**kwargs)


@method_decorator([login_required], name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "profile_edit.html"

    def form_valid(self, form):
        return super(UserUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(UserUpdateView, self).form_invalid(form)


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

    if vote_type == 'upvote':
        upvoted_targets.add(target)
    elif vote_type == 'downvote':
        downvoted_targets.add(target)

    target.update_points()
    return target.score


def vote(request, pk, question_or_answer):

    if not request.user.is_authenticated:
        return HttpResponse('Not logged in', status=401)

    if question_or_answer == 'question':
        target = Question.objects.get(pk=pk)
        if request.user.id == target.asked_by_id:
            return HttpResponseBadRequest('Same user', status=400)
    else:
        target = Answer.objects.get(pk=pk)
        if request.user.id == target.answered_by_id:
            return HttpResponseBadRequest('Same user',  status=400)

    if request.method == 'POST':
        vote_type = request.POST.get('vote_type')

        state = None
        if request.user.upvoted_questions.filter(pk=target.pk).exists():
            state = 'once_upvoted_question'
        elif request.user.downvoted_questions.filter(pk=target.pk).exists():
            state = 'once_downvoted_question'
        elif request.user.upvoted_answers.filter(pk=target.pk).exists():
            state = 'once_upvoted_answer'
        elif request.user.downvoted_answers.filter(pk=target.pk).exists():
            state = 'once_downvoted_answer'

        score = update_vote(request.user, target,
                            vote_type, question_or_answer)

        if state == 'once_upvoted_question' and vote_type == 'downvote':
            target.asked_by.question_once_upvote_now_downvote()
        elif state == 'once_downvoted_question' and vote_type == 'upvote':
            target.asked_by.question_once_downvote_now_upvote()

        elif question_or_answer == 'question' and vote_type == 'upvote':
            target.asked_by.question_vote_up()
        elif question_or_answer == 'question' and vote_type == 'downvote':
            target.asked_by.question_vote_down()

        elif vote_type == 'cancel_vote' and state == 'once_upvoted_question':
            target.asked_by.question_cancel_upvote()
        elif vote_type == 'cancel_vote' and state == 'once_downvoted_question':
            target.asked_by.question_cancel_downvote()

        elif state == 'once_upvoted_answer' and vote_type == 'downvote':
            request.user.points -= 1
            request.user.save()
            target.answered_by.answer_once_upvote_now_downvote()
        elif state == 'once_downvoted_answer' and vote_type == 'upvote':
            request.user.points += 1
            request.user.save()
            target.answered_by.answer_once_downvote_now_upvote()

        elif question_or_answer == 'answer' and vote_type == 'upvote':
            target.answered_by.answer_vote_up()
        elif question_or_answer == 'answer' and vote_type == 'downvote':
            request.user.points -= 1
            request.user.save()
            target.answered_by.answer_vote_down()

        elif vote_type == 'cancel_vote' and state == 'once_upvoted_answer':
            target.answered_by.answer_cancel_upvote()
        elif vote_type == 'cancel_vote' and state == 'once_downvoted_answer':
            target.answered_by.answer_cancel_downvote()

        return JsonResponse({'vote_type': vote_type, 'score': score})

    else:
        return HttpResponseBadRequest('The request is not POST',  status=400)


def accept(request, pk):
    if not request.user.is_authenticated:
        return HttpResponse('Not logged in', status=401)

    answer = Answer.objects.get(pk=pk)

    if answer.answered_by == answer.question.asked_by:
        return HttpResponseBadRequest('Answered by question-poster', status=400)

    if request.method == 'POST':
        accept_type = request.POST.get('accept_type')
        if accept_type == 'accept' and not answer.accepted:
            answer.accepted = True
            answer.save()
            answer.answered_by.accepted_answer()
            return JsonResponse({'accept_type': accept_type})
        elif accept_type == 'cancel_accept' and answer.accepted:
            answer.accepted = False
            answer.save()
            answer.answered_by.accepted_answer_cancel()
            return JsonResponse({'accept_type': accept_type})
    else:
        return HttpResponseBadRequest('The request is not POST',  status=400)
