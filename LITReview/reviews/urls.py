from django.urls import path
from . import views

urlpatterns = [
    path('create_review/', views.create_review_view, name='create_review'),
    path('create_ticket/', views.create_ticket_view, name='create_ticket'),
    path('edit_review/', views.edit_review_view, name='edit_review'),
    path('edit_ticket/', views.edit_ticket_view, name='edit_ticket'),
    path('feed/', views.feed_view, name='feed'),
    path('followers/', views.followers_view, name='followers'),
    path('update_profile_photo/', views.update_profile_photo_view, name='update_profile_photo'),
    path('user_profile/', views.user_profile_view, name='user_profile'),
]
