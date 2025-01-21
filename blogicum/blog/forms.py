from django import forms
from .models import Post
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import get_user_model


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'pub_date', 'author', 'location', 'category']


# class EditProfileForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')   

        


User = get_user_model()

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')