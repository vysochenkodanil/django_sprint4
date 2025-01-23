from django import forms
from django.contrib.auth import get_user_model
from .models import Post, Comment


User = get_user_model()


class CommentForm(forms.ModelForm):
    """Форма для создания и редактирования комментариев."""

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class PostForm(forms.ModelForm):
    """Форма для создания и редактирования постов."""

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'pub_date',
            'location',
            'category',
            'image',
        ]
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EditProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
