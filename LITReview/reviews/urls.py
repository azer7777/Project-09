from django.urls import path
from . import views

urlpatterns = [
    path("feed/", views.feed_view, name="feed"),
    path("create_ticket/", views.create_ticket_view, name="create_ticket"),
    path("create_review/<int:ticket_id>/", views.create_review_view, name="create_review"),
    path("create_ticket_and_review/", views.create_ticket_and_review_view, name="create_ticket_and_review"),
    path("edit_ticket/<int:ticket_id>/", views.edit_ticket_view, name="edit_ticket"),
    path("edit_review/<int:review_id>/", views.edit_review_view, name="edit_review"),
    path("delete_ticket/<int:ticket_id>/", views.delete_ticket_view, name="delete_ticket"),
    path("delete_review/<int:review_id>/", views.delete_review_view, name="delete_review"),
    path("subscriptions/", views.subscriptions_view, name="subscriptions"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow_user"),
    path("block_follower/<int:user_id>/", views.block_follower, name="block_follower"),
    path("user_profile/", views.user_profile_view, name="user_profile"),
    path("posts/", views.posts_view, name="posts"),
]
