# Generated by Django 5.1.3 on 2024-11-10 14:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('call_type', models.CharField(choices=[('voice', 'Voice'), ('video', 'Video')], max_length=5)),
                ('status', models.CharField(default='ongoing', max_length=20)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('caller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calls_initiated', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calls_received', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CallHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('call_type', models.CharField(choices=[('voice', 'Voice'), ('video', 'Video')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('duration', models.DurationField()),
                ('status', models.CharField(default='completed', max_length=20)),
                ('call', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat_app.call')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='call_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_group', models.BooleanField(default=False)),
                ('users', models.ManyToManyField(related_name='chat_rooms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_file', models.FileField(upload_to='chat_media/')),
                ('media_type', models.CharField(choices=[('text', 'Text'), ('image', 'Image'), ('video', 'Video')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('media_url', models.URLField(blank=True, null=True)),
                ('message_type', models.CharField(choices=[('text', 'Text'), ('image', 'Image'), ('video', 'Video')], default='text', max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('message', 'Message'), ('call', 'Call'), ('mention', 'Mention')], max_length=20)),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('last_seen', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship_type', models.CharField(choices=[('follow', 'Follow'), ('block', 'Block')], max_length=10)),
                ('status', models.CharField(default='active', max_length=20)),
                ('user_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_1_relationships', to=settings.AUTH_USER_MODEL)),
                ('user_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_2_relationships', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notifications_enabled', models.BooleanField(default=True)),
                ('privacy_mode', models.CharField(default='public', max_length=20)),
                ('theme', models.CharField(default='light', max_length=20)),
                ('sound_enabled', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
