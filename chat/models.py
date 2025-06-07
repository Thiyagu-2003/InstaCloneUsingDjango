from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class ThreadManager(models.Manager):
    def get_or_create_personal_thread(self, user1, user2):
        threads = self.filter(thread_type='personal', users=user1).filter(users=user2)
        if threads.exists():
            return threads.first(), False
        
        thread = self.create(thread_type='personal')
        thread.users.add(user1, user2)
        return thread, True

class Thread(models.Model):
    users = models.ManyToManyField(User, related_name='chat_threads')
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    thread_type = models.CharField(max_length=20, default='personal')
    archived_by = models.ManyToManyField(User, related_name='archived_threads', blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)

    objects = ThreadManager()  # Add this line to use the custom manager

    def __str__(self):
        if self.thread_type == 'personal' and self.users.count() == 2:
            user_list = list(self.users.all())
            return f'{user_list[0]} and {user_list[1]}'
        return self.name or f'Thread {self.id}'

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    deleted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='deleted_messages', blank=True)

    class Meta:
        ordering = ['created_at']

class MessageAttachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='chat_attachments/')
    file_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Attachment for message {self.message.id}'

class MessageReceipt(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='receipts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Receipt for message {self.message.id} by {self.user.username}'

