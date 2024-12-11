# urls.py
from django.urls import path
from mr_chat.profiles.views import logi,register,contact_us
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/register/', register, name='register'),
    path('home/login/', logi, name='login'),
    path('contact/', contact_us, name='contact_us')
]



