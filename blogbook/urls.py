from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from login_and_registration import views as login_and_registration_views
from blog import views as blog_views
from django.contrib.auth import logout



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #login/out urls taken from https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html
    url(r'^login/$', auth_views.LoginView.as_view(template_name="registration/login.html"), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page="/"), name='logout'),
    url(r'^signup/$', login_and_registration_views.signup, name='signup'),
    url(r'^post/$', blog_views.create_post, name='post'),
    url(r'^feed/$', blog_views.post_feed, name='feed'),
    url(r'^myposts/$', blog_views.myposts, name='myposts'),
    url(r'^myfeed/$', blog_views.myfeed, name='myfeed'),
    url(r'^user/(?P<username_of_user_of_page>.+)$', blog_views.userpage, name='userpage'),
    url(r'^home$', include('home.urls')),
    url(r'^$', include('home.urls')),
]
