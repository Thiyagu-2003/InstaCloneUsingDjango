# 📸 Instagram Clone Using Django

[![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.2.1-green?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Thiyagu-2003/InstaCloneUsingDjango?style=social)](https://github.com/Thiyagu-2003/InstaCloneUsingDjango/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Thiyagu-2003/InstaCloneUsingDjango?style=social)](https://github.com/Thiyagu-2003/InstaCloneUsingDjango/network/members)

Welcome to **Instagram Clone Using Django** — a sleek, full-featured social media web application built with **Django** and **Django Channels**, replicating core Instagram functionalities like photo sharing, following users, liking posts, and real-time chatting!

## 🌟 Demo


<div align="center"> <h4>🏠 Home Page</h4> <img src="https://github.com/user-attachments/assets/7798ae67-4a6f-4358-88c4-0bf59acf1fa8" width="70%" alt="Home page"/> <h4>👤 Profile Page</h4> <img src="https://github.com/user-attachments/assets/5469a379-6a6f-4972-bf8e-583da77f4193" width="70%" alt="Profile page"/> <h4>💬 Chat Room</h4> <img src="https://github.com/user-attachments/assets/a9f3b7d4-c406-4335-b2a5-53dfc2a62402" width="70%" alt="Chat room"/> <h4>📨 Chat Page</h4> <img src="https://github.com/user-attachments/assets/85c45af8-8eb8-4d5c-9e49-59fcf657eeda" width="70%" alt="Chat page"/> <h4>🔐 Login Page</h4> <img src="https://github.com/user-attachments/assets/29279f0d-d900-4515-9cbe-baf68784bd2b" width="70%" alt="Login page"/> </div>

## ✨ Features

### Core Functionality
- 🔐 **User Authentication & Profiles**  
  Complete user registration, login, logout, and profile management with customizable profile pictures

- 📷 **Photo Uploads with Captions**  
  Share your moments by uploading high-quality photos with engaging captions

- ❤️ **Likes & Comments**  
  Interactive engagement system with instant likes and threaded comments

- 💬 **Real-Time Chat**  
  Instant messaging powered by **Django Channels** and **WebSockets** for seamless communication

- 📱 **Responsive Design**  
  Mobile-first responsive UI built with **Bootstrap 5** ensuring optimal experience across all devices

### Additional Features
- 🔍 **Lists all User**
- 📊 **Activity Feed**
- 🔔 **Real-time Notifications**
- 🖼️ **Image Optimization**
- 👤 **Profile Customization**

## 🚀 Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.10+ | Backend programming language |
| **Django** | 5.2.1 | Web framework |
| **Django Channels** | 4.2 | Real-time WebSocket communication |
| **Redis** | 6.2+ | Message broker for async communication |
| **Daphne** | 4.2 | ASGI server for production |
| **Bootstrap** | 5.3 | Frontend styling framework |
| **Pillow** | Latest | Image processing and manipulation |
| **SQLite** | Default | Development database |
| **PostgreSQL** | Optional | Production database |

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

- **Python 3.10+**
- **Redis Server** (for real-time features)
- **Git** (for cloning the repository)
- **Virtual Environment** (recommended)

## 🎯 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Thiyagu-2003/InstaCloneUsingDjango.git
cd InstaCloneUsingDjango
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database Configuration (Optional)
DATABASE_URL=sqlite:///db.sqlite3

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### 5. Database Setup

```bash
# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser account (optional)
python manage.py createsuperuser
```

### 6. Start Redis Server

```bash
# Start Redis server (in a separate terminal)
redis-server

# Or on macOS with Homebrew:
brew services start redis

# Or on Ubuntu/Debian:
sudo systemctl start redis-server
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

### 8. Access the Application

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

## 📚 Usage Guide

### Getting Started
1. **Sign Up**: Create a new account with your email and password
2. **Profile Setup**: Add a profile picture and bio to personalize your account
3. **Discover Users**: Browse and follow other users to build your network
4. **Share Content**: Upload photos with captions to share your moments
5. **Chat**: Use real-time messaging to connect with other users

### Key Pages
- **Home Feed**: View posts from users
- **Profile**: Manage your account and profile
- **Explore**: Discover new users and trending content
- **Messages**: Access real-time chat functionality

## 🏗️ Project Structure

```
instagram_clone/                      # Root directory of the Django project
│
├── chat/                             # Django app for real-time chat functionality
│   ├── __pycache__/                  # Python cache files (auto-generated)
│   ├── chat/
│   │   └── templatetags/             # Custom template filters for chat
│   │       ├── __init__.py           # Makes this a Python package
│   │       └── chat_extras.py        # Contains custom template tags
│   ├── migrations/                   # Database migration files for chat
│   ├── templates/
│   │   └── chat/
│   │       └── chat.html             # HTML template for chat interface
│   ├── __init__.py                   # Marks chat as a Python module
│   ├── admin.py                      # Chat model admin configuration
│   ├── apps.py                       # App configuration
│   ├── consumers.py                  # WebSocket consumers for real-time chat
│   ├── models.py                     # Chat-related database models
│   ├── routing.py                    # WebSocket routing for chat
│   ├── signals.py                    # Signal handlers (e.g., for notifications)
│   ├── tests.py                      # Unit tests for chat
│   ├── urls.py                       # URL routing for chat views
│   └── views.py                      # Django views for chat
│
├── instagram/                        # Django project configuration directory
│   ├── __pycache__/                  # Python cache files
│   ├── __init__.py                   # Makes this a Python package
│   ├── asgi.py                       # ASGI entry point for asynchronous support (e.g., WebSockets)
│   ├── settings.py                   # Main project settings file
│   ├── urls.py                       # Root URL configuration
│   └── wsgi.py                       # WSGI entry point for deployment
│
├── media/                            # Uploaded media files
│   ├── chat_attachments/             # Attachments sent in chat
│   ├── posts/                        # Media files related to posts
│   ├── profile_pics/                 # User profile pictures
│   └── default.jpg                   # Default profile image
│
├── posts/                            # Django app for post creation and display
│   ├── __pycache__/                  # Python cache files
│   ├── migrations/                   # Database migration files for posts
│   ├── templates/
│   │   └── posts/
│   │       └── user_posts.html       # HTML template for user's posts
│   ├── __init__.py                   # Makes this a Python module
│   ├── admin.py                      # Admin interface config for posts
│   ├── apps.py                       # App configuration
│   ├── forms.py                      # Django forms for post creation
│   ├── models.py                     # Database models for posts
│   ├── tests.py                      # Unit tests for posts
│   ├── urls.py                       # URL patterns for posts
│   └── views.py                      # Views for post handling
│
├── static/                           # Static files (CSS, JS, etc.)
│   └── js/
│       └── notifications.js          # JavaScript for real-time notifications
│
├── users/                            # Django app for user management
│   ├── __pycache__/                  # Python cache files
│   ├── migrations/                   # Database migration files for users
│   ├── templates/
│   │   ├── registration/
│   │   │   └── login.html            # Login page template
│   │   └── users/
│   │       ├── logout.html           # Logout confirmation page
│   │       ├── profile.html          # Profile management page
│   │       └── register.html         # User registration page
│   ├── __init__.py                   # Marks users as a Python package
│   ├── admin.py                      # Admin interface config for users
│   ├── apps.py                       # App configuration
│   ├── forms.py                      # User-related forms
│   ├── models.py                     # User-related models
│   ├── tests.py                      # Unit tests for user features
│   ├── urls.py                       # URL patterns for user views
│   └── views.py                      # Views for user auth and profiles
│
├── venv/                             # Python virtual environment (contains packages/dependencies)
├── db.sqlite3                        # SQLite database file
├── LICENSE                           # License file for the project
├── manage.py                         # Django management script
├── README.md                         # Project documentation
└── requirements.txt                  # List of Python dependencies

```

## 💡 Real-Time Chat Implementation

This application leverages **Django Channels** with **Redis** as the message broker to enable real-time, bidirectional WebSocket communication. Key features include:

- **Instant Messaging**: Messages appear immediately without page refresh
- **Online Status**: See when users are online
- **Message History**: Persistent chat history stored in database
- **Typing Indicators**: Real-time typing notifications
- **Message Timestamps**: Precise message timing

### WebSocket Architecture
```python
# WebSocket connection flow
User A sends message → Django Channels → Redis → WebSocket → User B receives message
```

## 🎨 UI/UX Highlights

- **Modern Design**: Clean, Instagram-inspired interface
- **Responsive Layout**: Seamless experience across desktop, tablet, and mobile
- **Interactive Elements**: Smooth animations and hover effects
- **User-Friendly Navigation**: Intuitive menu and navigation structure
- **Accessibility**: WCAG compliant design principles
- **Performance Optimized**: Lazy loading and image optimization

## 🔧 Configuration Options

### Database Configuration
```python
# For PostgreSQL (Production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'instagram_clone',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Media Settings
```python
# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Maximum file size (5MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880
```

## 🚀 Deployment

### Production Setup
1. Set `DEBUG = False` in settings
2. Configure production database (PostgreSQL recommended)
3. Set up static file serving with WhiteNoise or CDN
4. Configure Redis for production
5. Set up ASGI server (Daphne or uWSGI)

### Docker Deployment (Optional)
```dockerfile
# Dockerfile example
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test posts
python manage.py test chat

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### How to Contribute
1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a new branch for your feature
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **Make** your changes and commit them
   ```bash
   git commit -m 'Add some amazing feature'
   ```
5. **Push** to your branch
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open** a Pull Request

## 📊 Future Enhancements

- [ ] **Stories Feature**: Instagram-style temporary stories
- [ ] **Video Support**: Upload and share videos
- [ ] **Advanced Search**: Search by hashtags and locations
- [ ] **Push Notifications**: Browser and mobile notifications
- [ ] **Dark Mode**: Toggle between light and dark themes
- [ ] **API Development**: RESTful API for mobile app integration
- [ ] **Machine Learning**: Content recommendation system

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.


## 📬 Contact & Support

Got questions or want to collaborate? Feel free to reach out!

- **GitHub**: [@Thiyagu-2003](https://github.com/Thiyagu-2003)
- **Email**: sthiyagu466@gmail.com
- **LinkedIn**: [Thiyagu S](https://www.linkedin.com/in/thiyagu-s-ai/)

## 🙏 Acknowledgments

- **Django Community** for the excellent framework
- **Bootstrap Team** for the responsive CSS framework
- **Redis Labs** for the in-memory data structure store
- **Contributors** who have helped improve this project

---

⭐ **If you found this project helpful, please give it a star!** ⭐

Made with ❤️ by [Thiyagu S](https://github.com/Thiyagu-2003)
