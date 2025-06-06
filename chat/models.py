from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ThreadManager(models.Manager):
    def get_or_create_personal_thread(self, user1, user2):
        # Filter personal threads involving both users
        threads = self.filter(thread_type='personal')
        threads = threads.filter(users__in=[user1, user2]).distinct()
        # Annotate with user count and filter threads with exactly 2 users
        threads = threads.annotate(u_count=models.Count('users')).filter(u_count=2)
        
        if threads.exists():
            return threads.first(), False
        else:
            # Create new personal thread and add users
            thread = self.create(thread_type='personal')
            thread.users.add(user1, user2)
            return thread, True

class Thread(models.Model):
    THREAD_TYPE = (
        ('personal', 'Personal'),
        ('group', 'Group'),
    )
    
    name = models.CharField(max_length=50, null=True, blank=True)
    thread_type = models.CharField(max_length=15, choices=THREAD_TYPE, default='personal')
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ThreadManager()

    def __str__(self):
        if self.thread_type == 'personal' and self.users.count() == 2:
            user_list = list(self.users.all())
            return f'{user_list[0]} and {user_list[1]}'
        return self.name or f'Thread {self.id}'

class Message(models.Model):
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # This ensures timestamp is saved
    delivered = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.text[:50]}"
