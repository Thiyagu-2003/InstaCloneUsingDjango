# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Message

# @receiver(post_save, sender=Message)
# def update_thread_timestamp(sender, instance, **kwargs):
#     # This will update Thread.updated_at due to auto_now=True
#     instance.thread.save(update_fields=['updated_at'])


from django.apps import AppConfig

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    def ready(self):
        import chat.signals  # ✅ Correct: Import inside ready()
