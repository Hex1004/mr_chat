from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from mr_chat.profiles.forms import RegistrationForm
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from mr_chat.profiles.models import Profile



def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            profile = form.save()  # Save the Profile (and User instance)
            user = profile.user  # Get the linked User instance
            login(request, user)  # Log in the user
            return redirect('/home/login/chatroom/')  # Redirect to chatroom after login
        else:
            messages.error(request, 'Registration failed. Please check the form for errors.')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def logi(request):
    # If the user is already authenticated, redirect to the chat page
    if request.user.is_authenticated:
        return redirect('chatroom_list')  # Redirect to the chat page if the user is logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Log in the user
            # Redirect to chat room after successful login
            return redirect('chatroom_list')  # Redirect to the chat page

        else:
            # Show an error message if authentication fails
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')

    return render(request, 'login.html')
