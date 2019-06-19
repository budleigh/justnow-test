import random
from dateutil import parser
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from django.views.decorators.http import require_POST
from justnow_app.forms import *
from justnow_app.models import *


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'index.html', {
        'auth_form': AuthForm(),
    })


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def entry(request, date=None):
    if not date:
        return redirect('home')

    day_entry, _ = Entry.objects.get_or_create(user=request.user, date=parser.parse(date))
    questions = day_entry.questions.all()
    questions = [question for question in questions]
    return render(request, 'entry.html', {
        'entry': day_entry,
        'date': date,
        'question': Question.objects.random() if random.random() > 0.1 else None,
        'asked_questions': questions,
    })


@login_required
def signout(request):
    logout(request)
    return redirect('index')


@csrf_exempt
@require_POST
@login_required
def save(request, date=None):
    day_entry, _ = Entry.objects.get_or_create(user=request.user, date=parser.parse(date))
    day_entry.text = request.POST['text']
    day_entry.save()
    return HttpResponse(status=201)


@csrf_exempt
@require_POST
@login_required
def ask(request, date=None):
    question_text = request.POST['question']
    entry, _ = Entry.objects.get_or_create(user=request.user, date=parser.parse(date))
    question = Question(
        entry=entry,
        text=question_text,
    )
    question.save()
    return HttpResponse(status=201)


@csrf_exempt
@require_POST
@login_required
def answer(request, question_id=None):
    question = Question.objects.get(pk=question_id)
    answer = Answer.objects.create(
        question=question,
        user=request.user,
        text=request.POST['answer'],
        private=False,
    )
    answer.save()
    return HttpResponse(status=201)


@require_POST
def auth(request):
    def sign_in(data):
        user = authenticate(username=data['email'], password=data['password'])
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Incorrect login details.')
            return redirect('index')

    def sign_up(data):
        try:
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password']
            )
            return sign_in(data)
        except IntegrityError:
            messages.add_message(request, messages.ERROR, 'User already exists.')
            return redirect('index')

    auth_form = AuthForm(request.POST)
    if auth_form.is_valid():
        data = auth_form.cleaned_data
        if data['type'] == 'UP':
            return sign_up(data)
        if data['type'] == 'IN':
            return sign_in(data)
    else:
        messages.add_message(request, messages.ERROR, 'There was an issue with your login details.')
        return redirect('index')
