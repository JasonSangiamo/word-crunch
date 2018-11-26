from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField
from django.dispatch import receiver
from django.db.models.signals import post_save

#import found at https://stackoverflow.com/questions/3206905/django-textfield-max-length-validation-for-modelform
class Profile(models.Model):
    user = AutoOneToOneField(User, primary_key = True, on_delete = models.CASCADE)
    following = models.ManyToManyField("self", symmetrical=False, related_name='following_users')
    blocked = models.ManyToManyField("self", symmetrical=False, related_name='blocked_users')

#sender reciever found at https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
#this code is what autoatmically creates a Profile on user creation
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Post(models.Model):
    author = models.ManyToManyField(Profile, related_name="post")
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    title.help_text = "Title your post  "
    description = models.CharField(max_length=100)
    description.help_text = "Provide a preview of the post (optional)"
    content = models.TextField()
    content.help_text = "Enter the post here"
    class Meta:
        ordering = ('-date',)
class Comment(models.Model):
    content = models.CharField(max_length=200)
    content.help_text = "Enter your comment here (200 characters or fewer)"
    post = models.ManyToManyField('Post', related_name="comments")
    author = models.ManyToManyField(Profile, related_name="comments")
    time = models.DateTimeField(auto_now_add=True)
class Upvote(models.Model):
    user = models.ManyToManyField(Profile, related_name = 'upvote')
    post = models.ManyToManyField(Post, related_name = 'upvote')
class Downvote(models.Model):
    user = models.ManyToManyField(Profile, related_name = 'downvote')
    post = models.ManyToManyField(Post, related_name = 'downvote')