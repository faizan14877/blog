from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #Api to post a comment
    path('postComment', views.postComment, name='postComment'),

    
    path('', views.blogHome, name='blog'),
    path('<slug:slug>/', views.blogPost, name='blogPost'),
]
