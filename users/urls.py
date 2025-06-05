# from django.urls import path
# from django.contrib.auth.views import LoginView, LogoutView
# from .views import register, profile

# urlpatterns = [
#     path('register/', register, name='register'),
#     # Update this line:
#     path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
#     path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
#     path('profile/', profile, name='profile'),
# ]

# from django.urls import path
# from django.contrib.auth.views import LogoutView
# from .views import register, profile

# urlpatterns = [
#     path('register/', register, name='register'),
#     path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),  # Updated this line
#     path('profile/', profile, name='profile'),
# ]


from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView  # Add this import
from .views import register, profile

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', profile, name='profile'),
]