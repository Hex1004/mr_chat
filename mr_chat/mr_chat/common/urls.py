from mr_chat.common.views import HomeView,HomePageView
from django.urls import path

urlpatterns = [
    path('', HomeView.as_view(), name='registration'),
    path('home/', HomePageView.as_view(), name='home'),
]
