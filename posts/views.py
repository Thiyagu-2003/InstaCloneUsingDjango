from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Post, Comment, Like
from .forms import PostForm, CommentForm

User = get_user_model()


# Home feed view (post creation + feed listing)
@login_required
def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'posts/home.html', context)


# Post detail view with comment form and like status
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('-created_date')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    is_liked = Like.objects.filter(post=post, user=request.user).exists()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': is_liked,
        'total_likes': post.likes.count(),
    }
    return render(request, 'posts/post_detail.html', context)


# ✅ AJAX handler for like/unlike functionality
@require_POST
@login_required
def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)

    liked = False
    existing_like = Like.objects.filter(post=post, user=request.user)
    if existing_like.exists():
        existing_like.delete()
    else:
        Like.objects.create(post=post, user=request.user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'like_count': post.likes.count()
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


# View to display posts by a specific user
@login_required
def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-date_posted')

    context = {
        'user': user,
        'posts': posts,
    }
    return render(request, 'posts/user_posts.html', context)
