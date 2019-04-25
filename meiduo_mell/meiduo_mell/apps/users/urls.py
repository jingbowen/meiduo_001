from django.conf.urls import url, include
from django.contrib import admin
from .views import RegisterView,UserNameContView,MobileCountView,LoginView


urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^usernames/(?P<username>[A-Za-z0-9-_]{5,20})/count/$', UserNameContView.as_view(), name='username'),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', MobileCountView.as_view(), name='mobile'),
    url(r'^login/$', LoginView.as_view(),name="login"),
]
