from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, Review, UserFollows
from .forms import ReviewForm, TicketForm, FollowUserForm
from django.contrib.auth.models import User


@login_required
def feed_view(request):
    # Get the user's followed users
    followed_users = UserFollows.objects.filter(follower=request.user).values_list('followed_user', flat=True)

    # Get posts and reviews of followed users
    posts = Ticket.objects.filter(author__in=followed_users)
    reviews = Review.objects.filter(user__in=followed_users)

    # Get reviews in response to the user's tickets
    responses = Review.objects.filter(ticket__author=request.user)

    # Merge posts and reviews into a single list and sort by creation time
    feed = sorted(list(posts) + list(reviews) + list(responses), key=lambda item: item.time_created, reverse=True)

    context = {
        'feed': feed,
    }
    return render(request, 'reviews/feed.html', context)


@login_required
def create_ticket_view(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.author = request.user
            ticket.save()
            messages.success(request, "Ticket created successfully.")
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

            messages.success(request, "Ticket and Review created successfully.")
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
            review.ticket = ticket  # Set the ticket for the review
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
            messages.success(request, "Review updated successfully.")
            return redirect('feed')
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
            messages.success(request, "Ticket updated successfully.")
            return redirect('feed')
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'reviews/edit_ticket.html', {'form': form, 'ticket': ticket})


@login_required
def delete_ticket_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, author=request.user)
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, "Ticket deleted successfully.")
        return redirect('feed')
    return render(request, 'reviews/delete_ticket.html', {'ticket': ticket})


@login_required
def delete_review_view(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Review deleted successfully.")
        return redirect('feed')
    return render(request, 'reviews/delete_review.html', {'review': review})


@login_required
def follow_user(request):
    if request.method == 'POST':
        followed_username = request.POST.get('followed_user')
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
    return redirect('feed')


@login_required
def unfollow_user(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    try:
        follow_relationship = UserFollows.objects.get(follower=request.user, followed_user=followed_user)
        follow_relationship.delete()
        messages.success(request, f"You have unfollowed {followed_user.username}.")
    except UserFollows.DoesNotExist:
        messages.error(request, f"You are not following {followed_user.username}.")
    return redirect('followers')


@login_required
def follow_user(request):
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
    return render(request, 'reviews/follow_user.html', {'form': form})


@login_required
def posts_view(request):
    user = request.user
    posts = Ticket.objects.filter(author=user).order_by('-created_at')
    return render(request, 'reviews/posts.html', {'posts': posts})


@login_required
def followers_view(request):
    followed_users = UserFollows.objects.filter(follower=request.user).values_list('followed_user', flat=True)
    followed_users = User.objects.filter(pk__in=followed_users)
    context = {
        'followed_users': followed_users,
    }
    return render(request, 'reviews/followers.html', context)


@login_required
def user_profile_view(request):
    user_posts = Ticket.objects.filter(author=request.user)
    context = {
        'user_posts': user_posts,
    }
    return render(request, 'reviews/user_profile.html', context)