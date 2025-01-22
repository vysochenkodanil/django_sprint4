from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'pub_date', 'location', 'category', 'image']
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')