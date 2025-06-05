from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat_home'),           # <- this one!
    path('send/', views.send_message, name='send_message'),
    path('<str:username>/', views.chat_view, name='chat'),
]
