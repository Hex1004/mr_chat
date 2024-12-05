from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'profile_picture']  # Only profile_title and profile_picture

class UserSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=True, label="Search for User")