from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, Review, UserFollows
from .forms import ReviewForm, TicketForm, FollowUserForm
from django.contrib.auth.models import User
from django.db.models import Q, Prefetch, F
from django.utils import timezone
from django.db.models.functions import Coalesce

@login_required
def feed_view(request):
    user = request.user
    followed_users = user.following.values_list('followed_user', flat=True)
    
    feed = Ticket.objects.filter(
        Q(author=user) | Q(author__in=followed_users) | Q(review__user=user)
    ).distinct().annotate(
        combined_created_at=Coalesce('review__time_edited', F('created_at'))
    ).order_by('-combined_created_at')

    return render(request, 'reviews/feed.html', {'feed': feed})


@login_required
def create_ticket_view(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.author = request.user
            ticket.save()
            return redirect('feed')
    else:
        ticket_form = TicketForm()
    
    context = {'ticket_form': ticket_form}
    return render(request, 'reviews/create_ticket.html', context)


@login_required
def create_ticket_and_review_view(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.author = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
    
    context = {'ticket_form': ticket_form, 'review_form': review_form}
    return render(request, 'reviews/create_ticket_and_review.html', context)


@login_required
def create_review_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    else:
        form = ReviewForm()

    return render(request, 'reviews/create_review.html', {'form': form, 'ticket': ticket})


@login_required
def edit_review_view(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            review.time_edited = timezone.now()
            return redirect('posts')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'reviews/edit_review.html', {'form': form, 'review': review})


@login_required
def edit_ticket_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, author=request.user)

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            ticket.time_edited = timezone.now()
            return redirect('posts')
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'reviews/edit_ticket.html', {'form': form, 'ticket': ticket})


@login_required
def delete_ticket_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, author=request.user)
    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')
    return render(request, 'reviews/delete_ticket.html', {'ticket': ticket})


@login_required
def delete_review_view(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        return redirect('posts')
    return render(request, 'reviews/delete_review.html', {'review': review})


@login_required
def subscriptions_view(request):
    if request.method == 'POST':
        form = FollowUserForm(request.POST)
        if form.is_valid():
            followed_username = form.cleaned_data['followed_user']
            try:
                followed_user = User.objects.get(username=followed_username)
                if followed_user == request.user:
                    messages.warning(request, "You cannot follow yourself.")
                else:
                    _, created = UserFollows.objects.get_or_create(follower=request.user, followed_user=followed_user)
                    if created:
                        messages.success(request, f"You are now following {followed_user.username}.")
                    else:
                        messages.info(request, f"You are already following {followed_user.username}.")
            except User.DoesNotExist:
                messages.error(request, f"The user '{followed_username}' does not exist.")
    else:
        form = FollowUserForm()

    followed_users = UserFollows.objects.filter(follower=request.user).values_list('followed_user', flat=True)
    followed_users = User.objects.filter(pk__in=followed_users)
    followers = UserFollows.objects.filter(followed_user=request.user).values_list('follower', flat=True)
    followers = User.objects.filter(pk__in=followers)

    context = {
        'followers': followers,
        'followed_users': followed_users,
        'following': followed_users,
        'form': form,
    }

    return render(request, 'reviews/subscriptions.html', context)


@login_required
def unfollow_user(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    try:
        follow_relationship = UserFollows.objects.get(follower=request.user, followed_user=followed_user)
        follow_relationship.delete()
        messages.success(request, f"You have unfollowed {followed_user.username}.")
    except UserFollows.DoesNotExist:
        messages.error(request, f"You are not following {followed_user.username}.")
    return redirect('subscriptions')


@login_required
def block_follower(request, user_id):
    try:
        follower_to_block = UserFollows.objects.get(followed_user=request.user, follower__id=user_id)
        follower_to_block.delete()
        messages.success(request, f"You have blocked {follower_to_block.follower.username}.")
    except UserFollows.DoesNotExist:
        messages.error(request, "Follower not found.")
    
    return redirect('subscriptions')


@login_required
def posts_view(request):
    user = request.user
    posts = Ticket.objects.filter(Q(author=user) | Q(review__user=user)).prefetch_related(
        Prefetch('review_set', queryset=Review.objects.filter(user=user))
    ).annotate(
        combined_created_at=Coalesce('review__time_edited', F('created_at'))
    ).order_by('-combined_created_at')

    return render(request, 'reviews/posts.html', {'posts': posts})


@login_required
def user_profile_view(request):
    user_posts = Ticket.objects.filter(author=request.user)
    context = {
        'user_posts': user_posts,
    }
    return render(request, 'reviews/user_profile.html', context)