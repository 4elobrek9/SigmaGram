from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/',
                               default='avatars/default.png')
    bio = models.TextField(max_length=500, blank=True)
    online_status = models.BooleanField(default=False)
    last_online = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sigma_gram_user'

    def __str__(self):
        return self.username


class Chat(models.Model):
    name = models.CharField(max_length=100, blank=True)
    participants = models.ManyToManyField(User, related_name='chats')
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='chat_avatars/',
                               blank=True,
                               null=True)

    def __str__(self):
        if self.is_group:
            return f"Group: {self.name}"
        participants = self.participants.all()
        return f"Chat between {participants[0]} and {participants[1]}"


class Message(models.Model):
    chat = models.ForeignKey(Chat,
                             related_name='messages',
                             on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender}: {self.content[:20]}..."
