"""
URL configuration for mr_chat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import mr_chat
from mr_chat.chat_app.views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('mr_chat.common.urls')),
    path('home/', include('mr_chat.common.urls')),
    path('home/register/', include('mr_chat.profiles.urls')),
    path('home/login/', include('mr_chat.profiles.urls')),
    path('home/login/chatroom/', include('mr_chat.profiles.urls')),
    path('home/login/chatroom/', ChatRoomListView.as_view(), name='chatroom_list'),
    path('home/login/chatroom/profile/', user_profile, name='user_profile'),
    path('home/login/', logout_view, name='logout'),
    path('home/login/chatroom/api/get-users/', search_user, name='get_users'),
    path('home/login/chatroom/settings/', settings_view, name='settings'),


]
