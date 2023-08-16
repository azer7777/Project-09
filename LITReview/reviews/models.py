from django.conf import settings
from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    time_edited = models.DateTimeField(auto_now=True)


class Review(models.Model):
    headline = models.CharField(max_length=200)
    body = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    time_edited = models.DateTimeField(auto_now=True)


class UserFollows(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="following", on_delete=models.CASCADE)
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="followers", on_delete=models.CASCADE)
    class Meta:
        unique_together = ('follower', 'followed_user',)