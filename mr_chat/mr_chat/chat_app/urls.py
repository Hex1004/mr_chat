from django.urls import path
from mr_chat.chat_app.views import *
from consumers import ChatConsumer



urlpatterns = [
    path('chatroom/', ChatRoomListView.as_view(), name='chatroom_list'),
    path('profile/', user_profile, name='user_profile'),
    path('logout/', logout_view, name='logout'),
    path('upload_profile_picture/', upload_profile_picture, name='upload_profile_picture'),
    path('api/search-user/', search_user, name='search_user'),
    path('add_to_chat/<int:user_id>/', add_user_to_chat, name='add_user_to_chat'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/new/', MessageCreateView.as_view(), name='message_create'),
    path('chatroom/<int:pk>/', ChatRoomDetailView.as_view(), name='chatroom_detail'),
    path('calls/', CallListView.as_view(), name='call_list'),
    path('call/<int:pk>/', CallDetailView.as_view(), name='call_detail'),
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('chat/<int:user_id>/', chat_room_detail, name='chat_room_detail'),
    path('api/search-user/api/send-invite/', send_invite, name='send_invite'),  # Add this line for the invite API
    path('api/accept-invite/<int:invite_id>/',accept_invite, name='accept_invite'),
    path('settings/',settings_view, name='settings'),
]
