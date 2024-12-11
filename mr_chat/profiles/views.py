from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from mr_chat.profiles.forms import RegistrationForm
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from mr_chat.profiles.models import Profile
from mr_chat.profiles.forms import ContactForm
from django.http import HttpResponseRedirect
from django.conf import settings
from mailjet_rest import Client


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            profile = form.save()  # Save the Profile (and User instance)
            user = profile.user  # Get the linked User instance

            # Send email to the new user
            subject = "Welcome to Mr.Chat!"
            message = (
                f"Hi {user.username},\n\n"
                "Thank you for registering at Chatroom. We're excited to have you on board! \n"
                "Feel free to log in and start chatting. If you have any questions, reply to this email.\n\n"
                "Best regards,\nThe Mr.Chat Team"
            )
            from_email = settings.EMAIL_HOST_USER  # Mailjet Sender Email
            recipient_list = [user.email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, "Registration successful! A welcome email has been sent.")
            except Exception as e:
                messages.warning(request, f"Registration successful, but email could not be sent: {e}")

            # Log in the user
            login(request, user)

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


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            # Retrieve cleaned data from the form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Prepare the dynamic variables to be inserted into the Mailjet template
            variables = {
                'name': name,
                'message': message,
                'subject': subject
            }

            try:
                # Initialize Mailjet client with your API credentials
                mailjet = Client(auth=(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD), version='v3.1')

                # Prepare the email data for sending to the user with the template
                data_user = {
                    'Messages': [
                        {
                            'From': {
                                'Email': email,  # Use the user's email as the sender
                                'Name': name,    # Use the user's name as the sender's name
                            },
                            'To': [
                                {'Email': email},  # Send the email to the user who submitted the form
                            ],
                            'Subject': subject,  # Subject from the form
                            'TemplateID': 6553975,  # Mailjet Template ID
                            'TemplateLanguage': True,  # Enable template language (dynamic content)
                            'Variables': variables  # Pass dynamic variables to the template
                        }
                    ]
                }

                # Prepare the email data for sending to the recipient (mrchat.contact@gmail.com) with raw content
                data_recipient = {
                    'Messages': [
                        {
                            'From': {
                                'Email': email,  # Use the user's email as the sender
                                'Name': name,    # Use the user's name as the sender's name
                            },
                            'To': [
                                {'Email': 'mrchat.contact@gmail.com'},  # Send the email to the recipient (mrchat.contact@gmail.com)
                            ],
                            'Subject': subject,  # Subject from the form
                            'TextPart': message,  # Send the raw message content to the recipient
                        }
                    ]
                }

                # Send the email to the user using the Mailjet API (with the template)
                response_user = mailjet.send.create(data=data_user)
                if response_user.status_code != 200:
                    error_details = response_user.json()
                    messages.error(request, f"An error occurred while sending the user's email: {error_details}")
                    print(f"Mailjet error (user): {error_details}")
                    return redirect('/#contact-us')

                # Send the raw email to the recipient (mrchat.contact@gmail.com)
                response_recipient = mailjet.send.create(data=data_recipient)
                if response_recipient.status_code != 200:
                    error_details = response_recipient.json()
                    messages.error(request, f"An error occurred while sending the recipient's email: {error_details}")
                    print(f"Mailjet error (recipient): {error_details}")
                    return redirect('/#contact-us')

                # If both emails were sent successfully
                messages.success(request, "Your message was sent successfully.")
                return redirect('/#contact-us')

            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
                print(f"Exception: {e}")
                return redirect('/#contact-us')

        else:
            # If form is not valid, show error messages
            messages.error(request, "There were errors in your form. Please correct them.")
            return redirect('/#contact-us')

    return HttpResponseRedirect('/')


