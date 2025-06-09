# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
#     re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
# ]

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Chat room WebSocket (personal 1-on-1 chats)
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),

    # Notifications WebSocket (for unread message count etc.)
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]
