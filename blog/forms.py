from django import forms

from .models import Post, Profile, Comment, Upvote, Downvote

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'content',)
class FollowUser(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['blocked','user']
        fields = ("following",)
class BlockUser(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['following','user']
        fields = ("blocked",)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        exclude = ('post','author','time')
class UpvoteForm(forms.ModelForm):
    class Meta:
        model = Upvote
        fields = ()
        exclude = ('user','post',)
class DownvoteForm(forms.ModelForm):
    class Meta:
        model = Downvote
        exclude = ('user','post')