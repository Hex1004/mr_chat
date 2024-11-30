from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        """Ensure passwords match."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        """Override save to create a User instance and link it to the Profile."""
        profile = super().save(commit=False)
        user = User.objects.create(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=make_password(self.cleaned_data['password1'])
        )
        profile.user = user  # Link the Profile to the User

        if commit:
            user.save()
            profile.save()

        return profile