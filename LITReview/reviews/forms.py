from django import forms
from .models import Review, Ticket
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfilePhotoForm(forms.ModelForm):
    profile_photo = forms.ImageField(label='Profile Photo')
    
    class Meta:
        model = User
        fields = ['profile_photo']
