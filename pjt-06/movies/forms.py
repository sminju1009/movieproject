from django import forms
from .models import Movie, Comment, Recomment


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        # fields = ('title', 'content',)
        exclude = ('user', 'like_users',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class RecommentForm(forms.ModelForm):
    class Meta:
        model = Recomment
        fields = ('content',)