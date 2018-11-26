from django.shortcuts import render
from .forms import PostForm, FollowUser, CommentForm, BlockUser, UpvoteForm, DownvoteForm
from django.shortcuts import render, redirect
from .models import Post, Profile, Comment, Upvote, Downvote
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from django.contrib.auth.models import User
#redirect found at https://stackoverflow.com/questions/39560175/django-redirect-to-same-page-after-post-method-using-class-based-views
from django.http import HttpResponseRedirect

# todo
# make follow/comment/upvote/downvote modular function that go into these functions
# fix comment redirect

@login_required(login_url='/')
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.user)
        if form.is_valid():
            #code taken from http://blog.appliedinformaticsinc.com/using-django-modelform-a-quick-guide/
            post = form.save(commit=False)
            post.save()

            #next two lines inspired by code at https://stackoverflow.com/questions/45407132/django-many-to-many-relationship-category
            post = Post.objects.get(pk=post.id)
            current_profile = Profile.objects.get(user = request.user)
            post.author.add(current_profile)
            messages.success(request, "Post Created!")
            return redirect('/feed/')
    else:
        form = PostForm()
        return render(request, "blog/create_post.html", {'form': form})

#this is the feed w/ all posts
@login_required(login_url='/')
def post_feed(request):
    comment_form = CommentForm()
    #this is correctly getting ids of blocked users for current user
    all_blocked_users = Profile.objects.filter(blocked_users = request.user.id)
    all_posts_to_display = Post.objects.exclude(author__in = all_blocked_users)
    if "comment" in request.POST:
        # running code to handle post requests for a post
        post_display_function(request)
    # need to delete old vote if user votes again!!!!!!!!!!!!!!!!!!!!
    if "upvote" in request.POST:
        # running code to handle post requests for a post
        post_display_function(request)
    if "downvote" in request.POST:
        # get form data (none)
        post_display_function(request)

    context = {'post_list':all_posts_to_display, 'blocked_user':all_blocked_users}
    return render(request, 'blog/post_feed.html', context)
@login_required(login_url='/')
def myposts(request):
    user = request.user
    current_user_object = Profile.objects.get(user=request.user)
    user_posts = Post.objects.all().filter(author=current_user_object)
    is_current_user = True
    context={'user_posts':user_posts, 'username':request.user,'is_current_user':is_current_user}
    if "comment" in request.POST:
        # running code to handle post requests for a post
        post_display_function(request)
    # need to delete old vote if user votes again!!!!!!!!!!!!!!!!!!!!
    if "upvote" in request.POST:
        # running code to handle post requests for a post
        post_display_function(request)
    if "downvote" in request.POST:
        # get form data (none)
        post_display_function(request)
    return render(request, 'blog/user_profile.html', context)
@login_required(login_url='/')
def userpage(request, username_of_user_of_page):
    profile_to_be_queried = Profile.objects.filter(user__username = username_of_user_of_page)
    user_posts = Post.objects.filter(author = profile_to_be_queried)
    form = FollowUser()
    comment_form = CommentForm()

    profile_of_page = Profile.objects.get(user__username=username_of_user_of_page)
    profile_of_current_user = Profile.objects.get(user__username=request.user)
    # if profile_of_current_user.blocked_set.filter(blocked=profile_of_page).exists():
    # checking if currently blocked
    if profile_of_page in profile_of_current_user.blocked.all():
        blocked = True
    else:
        blocked = False

    if profile_of_page in profile_of_current_user.following.all():
        followed = True
    else:
        followed = False

    if username_of_user_of_page == request.user.username:
        current_user = True
    else:
        current_user = False
    context = {'username': username_of_user_of_page, 'comment_form':comment_form , 'user_posts': user_posts,'followed':followed,'blocked':blocked,'current_user':current_user}
    context['test_string'] = "I AM FUNCTIONAL"
    
    
    
    f = open('helloworld.txt','a')
    f.write('FOLLOWING:' + str(context['followed']) +" and blocked: " + str(context['blocked']) + '\n')
    f.close()
    if request.method == "POST":
        #if follow button clicked
        if "follow" in request.POST:
            # get form data
            form = FollowUser(request.POST, request.user)
            # extract username of userpage from form
            username_of_profile_to_follow = request.POST.getlist('user_to_follow[]')[0]
            # get the profile of that username
            profile_to_follow = Profile.objects.get(user__username=username_of_profile_to_follow)
            # get profile of logged in user
            profile_who_will_follow_other_profile = Profile.objects.get(user__username=request.user)
            # creating m2m relationship
            profile_who_will_follow_other_profile.following.add(profile_to_follow)
            # context = {'username': username_of_user_of_page, 'user_posts': user_posts, 'form': form,}
            context['form'] = form
            context['followed'] = True
            f = open('helloworld.txt','a')
            f.write('HIT FOLLOW FOLLOWING:' + str(context['followed']) +" and blocked: " + str(context['blocked']))
            f.close()
            return render(request, 'blog/user_profile.html', context)
        if "unfllow" in request.POST:
            # get form data
            form = FollowUser(request.POST, request.user)
            # extract username of userpage from form
            username_of_profile_to_follow = request.POST.getlist('user_to_unfollow[]')[0]
            # get the profile of that username
            profile_to_follow = Profile.objects.get(user__username=username_of_profile_to_follow)
            # get profile of logged in user
            profile_who_will_follow_other_profile = Profile.objects.get(user__username=request.user)
            # creating m2m relationship
            profile_who_will_follow_other_profile.following.remove(profile_to_follow)
            # context = {'username': username_of_user_of_page, 'user_posts': user_posts, 'form': form,}
            context['form'] = form
            context['followed'] = False
            f = open('helloworld.txt','a')
            f.write('HIT UNFOLLOW FOLLOWING:' + str(context['followed']) +" and blocked: " + str(context['blocked']))
            f.close()
            return render(request, 'blog/user_profile.html', context)
        #if block button hit
        if "block" in request.POST:
            # get form data
            form = BlockUser(request.POST, request.user)
            # extract username of userpage from form
            username_of_profile_to_block = request.POST.getlist('user_to_block[]')[0]
            # get the profile of that username
            profile_to_block = Profile.objects.get(user__username=username_of_profile_to_block)
            # get profile of logged in user
            profile_who_will_block_other_profile = Profile.objects.get(user__username=request.user)
            # creating m2m relationship
            profile_who_will_block_other_profile.blocked.add(profile_to_block)
            context['blocked'] = True
            context['form'] = form
            f = open('helloworld.txt','a')
            f.write('HIT BLOCK FOLLOWING:' + str(context['followed']) +" and blocked: " + str(context['blocked']))
            f.close()
            return render(request, 'blog/user_profile.html', context)
        #if comment button hit do...
        if "unblck" in request.POST:
            form = BlockUser(request.POST, request.user)
            # extract username of userpage from form
            username_of_profile_to_unblock = request.POST.getlist('user_to_unblock[]')[0]
            # get the profile of that username
            profile_to_unblock = Profile.objects.get(user__username=username_of_profile_to_unblock)
            # get profile of logged in user
            profile_who_will_unblock_other_profile = Profile.objects.get(user__username=request.user)
            # creating m2m relationship
            profile_who_will_unblock_other_profile.blocked.remove(profile_to_unblock)
            context['form'] = form
            context['blocked'] = False
            f = open('helloworld.txt','a')
            f.write('HIT UNBLOCK FOLLOWING:' + str(context['followed']) +" and blocked: " + str(context['blocked']))
            f.close()
            return render(request, 'blog/user_profile.html', context)
        if "comment" in request.POST:
            #running code to handle post requests for a post
            post_display_function(request)
            # context = {'username':username_of_user_of_page, 'user_posts': user_posts}
            return render(request, 'blog/user_profile.html', context)

        #need to delete old vote if user votes again!!!!!!!!!!!!!!!!!!!!
        if "upvote" in request.POST:
            #running code to handle post requests for a post
            post_display_function(request)
            # context = {'username':username_of_user_of_page, 'user_posts': user_posts}
            return render(request, 'blog/user_profile.html', context)
        if "downvote" in request.POST:
            #get form data (none)
            post_display_function(request)
            # context = {'username': username_of_user_of_page, 'user_posts': user_posts}
            return render(request, 'blog/user_profile.html', context)
    # context = {'username': username_of_user_of_page, 'user_posts': user_posts, 'form': form,
   # 'comment_form': comment_form}
    #EXPERIMENT
    #check if user is already followed/blocked:


    #end EXPERIMENT
    return render(request, 'blog/user_profile.html', context)
@login_required(login_url='/')
def myfeed(request):
    # current_user_proifle = Profile.objects.get(user = request.user)
    all_followed_users = Profile.objects.filter(following_users = request.user.id)

    all_posts_to_display = Post.objects.filter(author__in = all_followed_users)
    if "comment" in request.POST:
        # running code to handle post requests for a post
        post_display_function(request)

    context = {'post_list': all_posts_to_display, 'followed_users': all_followed_users}
    return render(request, 'blog/my_feed.html', context)


#these are functions that all posts, myfeed, and userpage must all have so they are put here for modularity
def post_display_function(request):
    if "comment" in request.POST:
        # get form data
        form = CommentForm(request.POST, request.user)
        # extract content of comment and user
        comment_author_name = request.POST.getlist('current_user[]')[0]
        comment_author_object = Profile.objects.get(user=request.user)
        comment_content = request.POST.getlist('content[]')[0]
        comment = Comment(content=comment_content)
        comment.save()

        # connects author to comment
        comment_author_object.comments.add(comment)

        # connects comment to post
        post_id_to_associate = request.POST.getlist('post_id[]')[0]
        post_to_associate = Post.objects.get(id=post_id_to_associate)
        comment.post.add(post_to_associate)
    if "upvote" in request.POST:

        # getting voter profile to associate
        voter_object = Profile.objects.get(user=request.user)

        # getting post object
        post_id = request.POST.getlist('post[]')[0]
        post_object = Post.objects.get(id=post_id)

        #deleting current vote if it exists
        Upvote.objects.filter(user=voter_object).filter(post=post_object).delete()
        Downvote.objects.filter(user=voter_object).filter(post=post_object).delete()


        # get form data (none)
        form = UpvoteForm(request.POST, request.user)



        # creating upvote object
        upvote_object = Upvote()
        upvote_object.save()

        # associating upvote with user
        upvote_object.user.add(voter_object)

        # associating upvote with post
        upvote_object.post.add(post_object)
    if "downvote" in request.POST:

        # getting voter profile to associate
        voter_object = Profile.objects.get(user=request.user)

        # getting post object
        post_id = request.POST.getlist('post[]')[0]
        post_object = Post.objects.get(id=post_id)

        # deleting current vote if it exists
        Upvote.objects.filter(user=voter_object).filter(post=post_object).delete()
        Downvote.objects.filter(user=voter_object).filter(post=post_object).delete()

        # get form data (none)
        form = DownvoteForm(request.POST, request.user)



        # creating upvote object
        downvote_object = Downvote()
        downvote_object.save()

        # associating upvote with user
        downvote_object.user.add(voter_object)

        # associating upvote with post
        downvote_object.post.add(post_object)

