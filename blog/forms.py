from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'post_type')

    def clean_title(self):
        data = self.cleaned_data['title']
        if not data.startswith("test"):
            raise forms.ValidationError("Title must start with 'test'")
        return data

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('user', 'text',)