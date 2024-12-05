from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django's built-in User model
    unique_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # Profile picture
    status = models.CharField(max_length=255, null=True, blank=True)  # User's status message
    last_seen = models.DateTimeField(auto_now=True)  # Automatically set the timestamp when the user was last seen
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on user creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on every save

    def __str__(self):
        return self.user.username


class ChatInvite(models.Model):
    sender = models.ForeignKey(User, related_name='sent_invites', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_invites', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted')], default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(ChatInvite, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages_sent', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)




class Call(models.Model):
    VOICE = 'voice'
    VIDEO = 'video'
    CALL_TYPES = [
        (VOICE, 'Voice'),
        (VIDEO, 'Video'),
    ]

    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calls_initiated')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calls_received')
    call_type = models.CharField(max_length=5, choices=CALL_TYPES)
    status = models.CharField(max_length=20, default='ongoing')  # Ongoing, completed, missed, etc.
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Call from {self.caller.username} to {self.receiver.username}"


class Notification(models.Model):
    MESSAGE = 'message'
    CALL = 'call'
    MENTION = 'mention'
    NOTIFICATION_TYPES = [
        (MESSAGE, 'Message'),
        (CALL, 'Call'),
        (MENTION, 'Mention'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    content = models.TextField()  # Content of the notification (e.g., "New message from [User]")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.content[:20]}"


class UserRelationship(models.Model):
    FOLLOW = 'follow'
    BLOCK = 'block'
    RELATIONSHIP_TYPES = [
        (FOLLOW, 'Follow'),
        (BLOCK, 'Block'),
    ]

    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_1_relationships')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_2_relationships')
    relationship_type = models.CharField(max_length=10, choices=RELATIONSHIP_TYPES)
    status = models.CharField(max_length=20, default='active')  # Active or inactive relationship

    def __str__(self):
        return f"{self.user_1.username} {self.get_relationship_type_display()} {self.user_2.username}"


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notifications_enabled = models.BooleanField(default=True)
    privacy_mode = models.CharField(max_length=20, default='public')  # public/private
    theme = models.CharField(max_length=20, default='light')  # light/dark theme
    sound_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Settings for {self.user.username}"


class CallHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='call_history')
    call = models.ForeignKey(Call, on_delete=models.CASCADE)
    call_type = models.CharField(max_length=10, choices=Call.CALL_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()  # Call duration
    status = models.CharField(max_length=20, default='completed')  # Call status (completed, missed, etc.)

    def __str__(self):
        return f"History for {self.user.username}: {self.call_type} call at {self.timestamp}"
