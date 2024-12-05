from django.contrib import admin
from mr_chat.profiles.models import  Profile
from unfold.admin import ModelAdmin



@admin.register(Profile)
class ModelNameAdmin(ModelAdmin):
    pass

