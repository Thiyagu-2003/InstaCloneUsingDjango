import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth import get_user_model
from .models import Thread, Message

User = get_user_model()

@login_required
def user_list(request):
    """List all users except current user (no select_related needed)"""
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/user_list.html', {'users': users})

@login_required
def chat_view(request, username=None):
    """Main chat view with thread, messages, and WebSocket room setup"""
    all_users = User.objects.exclude(id=request.user.id)
    threads = Thread.objects.filter(users=request.user).order_by('-updated_at')

    receiver = None
    chat_messages = []
    room_name = None

    if username:
        receiver = get_object_or_404(User, username=username)
        thread, created = Thread.objects.get_or_create_personal_thread(request.user, receiver)
        chat_messages = thread.messages.all().order_by('created')
        thread.messages.filter(sender=receiver, read=False).update(read=True)

        # 🔑 Ensure room name is based on sorted user IDs for WebSocket
        user_ids = sorted([request.user.id, receiver.id])
        room_name = f"{user_ids[0]}_{user_ids[1]}"

    context = {
        'all_users': all_users,
        'threads': threads,
        'receiver': receiver,
        'chat_messages': chat_messages,
        'room_name': room_name,  # ✅ now available in chat.html
    }
    return render(request, 'chat/chat.html', context)

@login_required
def send_message(request):
    """Handle message sending"""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        data = json.loads(request.body)
        receiver_username = data.get('receiver')
        message_text = data.get('message')
    except Exception:
        receiver_username = request.POST.get('receiver')
        message_text = request.POST.get('message')

    if not receiver_username or not message_text:
        return JsonResponse(
            {'status': 'error', 'message': 'Missing receiver or message'},
            status=400
        )

    try:
        receiver = get_object_or_404(User, username=receiver_username)
        thread, created = Thread.objects.get_or_create_personal_thread(request.user, receiver)

        message = Message.objects.create(
            thread=thread,
            sender=request.user,
            text=message_text
        )

        return JsonResponse({
            'status': 'success',
            'message': message.text,
            'sender': request.user.username,
            'sender_profile_pic': request.user.profile_pic.url if request.user.profile_pic else '/static/default_profile.jpg',
            'created': message.created.strftime('%Y-%m-%d %H:%M:%S'),
            'message_id': message.id,
        })

    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'message': str(e)},
            status=400
        )
