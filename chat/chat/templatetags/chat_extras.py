from django import template
from django.contrib.auth import get_user_model

register = template.Library()
User = get_user_model()

@register.filter
def get_user_by_username(users, username):
    try:
        return users.get(username=username)
    except User.DoesNotExist:
        return None
