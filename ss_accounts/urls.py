from django.urls import path
from django.contrib.auth.views import LogoutView,LoginView
from . import views
from django.conf.urls import url
urlpatterns = [
    
    url(r'^dashboard/$', views.dash, name='dashboard'),
    url(r'^login/$', LoginView.as_view(template_name='ss_accounts/login.html'),name='login'), 
    url(r'^logout/$', LogoutView.as_view(template_name='logout.html'),name='logout'),
]
