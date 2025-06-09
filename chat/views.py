# import json
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse, HttpResponseNotAllowed
# from django.contrib.auth import get_user_model
# from .models import Thread, Message, MessageAttachment
# from django.db.models import Count, Q

# User = get_user_model()

# @login_required
# def user_list(request):
#     """List all users except current user (no select_related needed)"""
#     users = User.objects.exclude(id=request.user.id)
#     return render(request, 'chat/user_list.html', {'users': users})

# @login_required
# def chat_view(request, username=None):
#     all_users = User.objects.exclude(id=request.user.id)
#     threads = Thread.objects.filter(users=request.user).order_by('-updated_at')

#     # Calculate unread counts for each thread
#     for thread in threads:
#         # Get the other participant in the thread
#         other_user = thread.users.exclude(id=request.user.id).first()
#         thread.last_message = thread.messages.last()
#         # Count unread messages from the other participant
#         thread.unread_count = thread.messages.filter(
#             sender=other_user,
#             read=False
#         ).count() if other_user else 0

#     receiver = None
#     chat_messages = []
#     room_name = None

#     if username:
#         receiver = get_object_or_404(User, username=username)
#         thread, created = Thread.objects.get_or_create_personal_thread(request.user, receiver)
#         chat_messages = thread.messages.all().order_by('created_at')
#         # Mark messages as read when opening the chat
#         thread.messages.filter(sender=receiver, read=False).update(read=True)

#         # Generate room name for WebSocket
#         user_ids = sorted([request.user.id, receiver.id])
#         room_name = f"{user_ids[0]}_{user_ids[1]}"

#     context = {
#         'all_users': all_users,
#         'threads': threads,
#         'receiver': receiver,
#         'chat_messages': chat_messages,
#         'room_name': room_name,
#     }
#     return render(request, 'chat/chat.html', context)

# @login_required
# def send_message(request):
#     if request.method == 'POST':
#         receiver_username = request.POST.get('receiver')
#         message_text = request.POST.get('message')
        
#         try:
#             receiver = User.objects.get(username=receiver_username)
#             # Unpack the tuple returned by get_or_create_personal_thread
#             thread, created = Thread.objects.get_or_create_personal_thread(request.user, receiver)
            
#             # Create and save the message with timestamp
#             message = Message.objects.create(
#                 thread=thread,  # Now using just the thread object
#                 sender=request.user,
#                 text=message_text
#             )
            
#             # Handle file attachments
#             for f in request.FILES.getlist('attachments'):
#                 MessageAttachment.objects.create(
#                     message=message,
#                     file=f,
#                     file_type=f.content_type
#                 )
            
#             return JsonResponse({
#                 'status': 'success',
#                 'message': message.text,
#                 'message_id': message.id,
#                 'created_at': message.created_at.isoformat(),
#                 'sender': request.user.username,
#                 'sender_profile_pic': request.user.profile_pic.url if request.user.profile_pic else None
#             })
            
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'error': str(e)})
    
#     return JsonResponse({'status': 'error', 'error': 'Invalid request method'})



import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth import get_user_model
from .models import Thread, Message, MessageAttachment
from django.db.models import Count, Q

User = get_user_model()

@login_required
def user_list(request):
    """List all users except current user (no select_related needed)"""
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/user_list.html', {'users': users})

@login_required
def chat_view(request, username=None):
    all_users = User.objects.exclude(id=request.user.id)
    threads = Thread.objects.filter(users=request.user).order_by('-updated_at')

    # Calculate unread counts for each thread
    for thread in threads:
        # Get the other participant in the thread
        other_user = thread.users.exclude(id=request.user.id).first()
        thread.last_message = thread.messages.last()
        # Count unread messages from the other participant
        thread.unread_count = thread.messages.filter(
            sender=other_user,
            read=False
        ).count() if other_user else 0

    receiver = None
    chat_messages = []
    room_name = None

    if username:
        receiver = get_object_or_404(User, username=username)
        thread, created = Thread.objects.get_or_create_personal_thread(request.user, receiver)
        chat_messages = thread.messages.all().order_by('created_at')
        # Mark messages as read when opening the chat
        thread.messages.filter(sender=receiver, read=False).update(read=True)

        # Generate room name for WebSocket
        user_ids = sorted([request.user.id, receiver.id])
        room_name = f"{user_ids[0]}_{user_ids[1]}"

    context = {
        'all_users': all_users,
        'threads': threads,
        'receiver': receiver,
        'chat_messages': chat_messages,
        'room_name': room_name,
    }
    return render(request, 'chat/chat.html', context)

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        message_text = request.POST.get('message')
        
        try:
            receiver = User.objects.get(username=receiver_username)
            thread, created = Thread.objects.get_or_create_personal_thread(request.user, receiver)
            
            message = Message.objects.create(
                thread=thread,
                sender=request.user,
                text=message_text
            )

            for f in request.FILES.getlist('attachments'):
                MessageAttachment.objects.create(
                    message=message,
                    file=f,
                    file_type=f.content_type
                )

            # WebSocket broadcast via Django Channels
            channel_layer = get_channel_layer()
            room_name = "_".join(sorted([str(request.user.id), str(receiver.id)]))
            async_to_sync(channel_layer.group_send)(
                f"chat_{room_name}",
                {
                    'type': 'chat_message',
                    'message': message.text,
                    'sender': request.user.username,
                    'sender_profile_pic': request.user.profile_pic.url if request.user.profile_pic else '/static/default_profile.jpg',
                    'message_id': message.id,
                    'timestamp': message.created_at.isoformat(),
                    'receiver': receiver.username,
                }
            )

            return JsonResponse({
                'status': 'success',
                'message': message.text,
                'message_id': message.id,
                'created_at': message.created_at.isoformat(),
                'sender': request.user.username,
                'sender_profile_pic': request.user.profile_pic.url if request.user.profile_pic else None
            })
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)})

    return JsonResponse({'status': 'error', 'error': 'Invalid request method'})
