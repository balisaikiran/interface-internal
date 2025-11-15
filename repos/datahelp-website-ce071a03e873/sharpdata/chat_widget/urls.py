from django.urls import path
from . import views

urlpatterns = [
    path('list_conversations', views.list_conversations, name='list_conversations'),
    path('get_chats', views.get_previous_chats, name='get_chats'),
    path('chat', views.chat, name='chat'),
    path('send_message', views.send_message, name='send_message')
]
