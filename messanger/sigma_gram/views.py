from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.db.models import Subquery, OuterRef
from .models import Chat, Message


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f'Аккаунт {username} создан!')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'sigma_gram/register.html', {'form': form})


@login_required
def index(request):
    last_messages = Message.objects.filter(
        chat=OuterRef('pk')
    ).order_by('-timestamp')[:1]

    chats = Chat.objects.filter(
        participants=request.user
    ).annotate(
        last_message_text=Subquery(last_messages.values('text')),
        last_message_time=Subquery(last_messages.values('timestamp'))
    ).order_by('-last_message_time')

    context = {
        'chats': chats,
        'user': request.user
    }
    return render(request, 'sigma_gram/index.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = AuthenticationForm()

    return render(request, 'sigma_gram/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
