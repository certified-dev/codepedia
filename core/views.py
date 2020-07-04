from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from.models import Question

class RecentQuestionView(ListView):
    model = Question
    context_object_name = "questions"
    template_name = "home.html"
