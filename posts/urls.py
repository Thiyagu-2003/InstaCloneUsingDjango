from django.urls import path
from .views import home, post_detail, like_post, user_posts

urlpatterns = [
    path('', home, name='home'),
    path('post/<int:pk>/', post_detail, name='post-detail'),
    path('like/', like_post, name='like-post'),
    path('user/<str:username>/', user_posts, name='user-posts'),
]