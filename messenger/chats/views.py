from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from accounts.models import CustomUser


@login_required
def chats_list(request):
    chats = request.user.chats.all()
    return render(request, 'chats/list.html', {'chats': chats})


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(chat=chat, sender=request.user, text=text)
            return redirect('chat_detail', chat_id=chat.id)

    messages = chat.messages.all()
    return render(request, 'chats/detail.html', {'chat': chat,
                                                 'messages': messages})


@login_required
def start_chat(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    chat = Chat.objects.filter(participants=request.user).filter(participants=user).first()
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, user)
    return redirect('chat_detail', chat_id=chat.id)


@login_required
def user_list(request):
    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'chats/user_list.html', {'users': users})
