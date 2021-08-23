from django.urls import path, include
from django.urls.resolvers import URLPattern
from . import views

app_name = 'user_account'

urlpatterns = [
    path('', views.profile, name='profile')
]