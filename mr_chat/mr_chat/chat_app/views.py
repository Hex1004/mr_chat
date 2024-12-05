import profile

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

from .models import UserProfile, Message, ChatRoom, Call, Notification
from django.urls import reverse_lazy
from mr_chat.chat_app.forms import UserProfileForm
from django.contrib import messages
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from mr_chat.profiles.models import Profile
from .models import ChatInvite
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

@login_required
def user_profile(request):
    # Get or create the user's profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Generate a unique number if it doesn't exist
    if not user_profile.unique_number:
        user_profile.unique_number = get_random_string(length=4, allowed_chars='0123456789')
        user_profile.save()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')  # Redirect to the same page after successful update
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'users.html', {
        'user': request.user,  # Access the user model for username/email
        'profile': user_profile,  # Access the user profile for other fields
        'form': form,
    })


@login_required
def settings_view(request):
    return  render(request, 'settings.html')

@login_required
def user_profile_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = user.userprofile
    return render(request, 'users.html', {
        'user': user,
        'profile': user_profile,
    })


@login_required
def send_invite(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse the incoming JSON data
        user_id = data.get('id')  # Get the user id from the request
        username = data.get('username')  # Get the username from the request

        receiver = get_object_or_404(User, id=user_id)  # Get the user by ID

        # Create a new invite
        invite = ChatInvite.objects.create(sender=request.user, receiver=receiver)

        # Respond with a success message
        return JsonResponse({
            'status': 'success',
            'message': f'Invitation sent to {username}.'
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

@login_required
def view_invites(request):
    invites = ChatInvite.objects.filter(receiver=request.user, status='pending')
    return render(request, 'invite.html', {'invites': invites})


@login_required
def accept_invite(request, invite_id):
    invite = get_object_or_404(ChatInvite, id=invite_id, receiver=request.user)
    invite.status = 'accepted'
    invite.save()
    return redirect('chatroom_list')




def logout_view(request):
    # Log out the user
    logout(request)

    # Add a success message
    messages.success(request, 'You have successfully logged out.')

    # Render the logout page with the success message
    return render(request, 'logout.html')


@login_required
def upload_profile_picture(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST' and request.FILES.get('profilePicture'):
        user_profile.profile_picture = request.FILES['profilePicture']
        user_profile.save()
        return redirect('user_profile')  # Redirect to the user profile page
    return redirect('user_profile')



def set_cookie(request):
    response = HttpResponse("Cookie has been set")
    response.set_cookie('my_cookie', 'cookie_value', max_age=3600)  # Set a cookie with a 1-hour expiration time
    return response


def get_cookie(request):
    cookie_value = request.COOKIES.get('my_cookie', 'default_value')  # Get the cookie or return a default value if not found
    return HttpResponse(f"The value of 'my_cookie' is: {cookie_value}")

def delete_cookie(request):
    response = HttpResponse("Cookie has been deleted")
    response.delete_cookie('my_cookie')  # Delete the 'my_cookie' cookie
    return response


@login_required
def edit_profile(request):
    # Get the user's profile (or create one if it doesn't exist)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Handle form submission
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')  # Redirect to the profile page after saving changes
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'users.html', {'form': form})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()

class MessageListView(ListView):
    model = Message
    template_name = 'chat_page.html'  # Replace with your template path
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)

class MessageCreateView(CreateView):
    model = Message
    fields = ['receiver', 'content', 'message_type', 'media_url']
    template_name = 'chat_page.html'  # Replace with your template path
    success_url = reverse_lazy('message_list')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)





def search_user(request):
    username_query = request.GET.get('username', '').strip()  # Retrieve username query parameter
    if username_query:
        # Filter profiles containing the username query (case-insensitive)
        users = Profile.objects.filter(username__icontains=username_query)
        # Prepare a response with user data (id, username)
        user_data = [{'email': user.email, 'username': user.username} for user in users]
        return JsonResponse(user_data, safe=False)  # Return users as JSON response
    else:
        return JsonResponse([], safe=False)

@login_required
def add_user_to_chat(request, user_email):
    user_to_add = User.objects.get(email=user_email)
    chat_room, created = ChatRoom.objects.get_or_create(users__in=[request.user, user_to_add])

    if created:
        # Optionally, add any initial message when the chat is created.
        chat_room.save()

    return redirect('chat_room_detail', chat_room_id=chat_room.id)


@login_required
def chat_room_detail(request, chat_room_id):
    chat_room = ChatRoom.objects.get(id=chat_room_id)
    messages = chat_room.messages.all()  # Assuming you have a Message model
    return render(request, 'chat_page.html', {
        'chat_room': chat_room,
        'messages': messages,
    })


@login_required
def chatPage(request, user_id):
    # Find the chat room between the logged-in user and the specified user_id
    chat_room = get_object_or_404(ChatRoom, users__id=user_id)

    # Get all messages related to the chat room
    messages = chat_room.messages.all()  # Assuming you have a Message model

    # Pass the necessary data to the template
    return render(request, 'chat_page.html', {
        'chat_room': chat_room,
        'messages': messages,
        'user_id': user_id  # Pass the user ID to the template
    })



class ChatRoomListView(LoginRequiredMixin, ListView):
    model = ChatRoom
    template_name = 'chat_page.html'  # Path to your chat page template
    context_object_name = 'chatroom'  # Name for use in the template

    def get_queryset(self):
        # Ensure the user is authenticated before accessing chat rooms
        if self.request.user.is_authenticated:
            # Return chat rooms that include the current user
            return ChatRoom.objects.filter(users=self.request.user)
        else:
            # If user is not authenticated, return an empty queryset (or redirect)
            return ChatRoom.objects.none()


class ChatRoomDetailView(DetailView):
    model = ChatRoom
    template_name = 'chat_page.html'  # Replace with your template path
    context_object_name = 'chatroom'


class CallListView(ListView):
    model = Call
    template_name = 'call_list.html'  # Replace with your template path
    context_object_name = 'calls'

    def get_queryset(self):
        return Call.objects.filter(caller=self.request.user)

class CallDetailView(DetailView):
    model = Call
    template_name = 'chat_page.html'  # Replace with your template path
    context_object_name = 'call'

class NotificationListView(ListView):
    model = Notification
    template_name = 'chat_page.html'  # Replace with your template path
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False)
