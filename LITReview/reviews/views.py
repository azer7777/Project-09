from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket, Review, UserFollows
from .forms import ReviewForm, TicketForm
from django.db.models import F, Q

@login_required
def create_review_view(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('feed')
    else:
        form = ReviewForm()
    return render(request, 'reviews/create_review.html', {'form': form})

@login_required
def create_ticket_view(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.author = request.user
            ticket.save()
            return redirect('feed')
    else:
        form = TicketForm()
    return render(request, 'reviews/create_ticket.html', {'form': form})

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
            review.save()

            return redirect('feed')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
    return render(request, 'reviews/create_ticket.html', {'ticket_form': ticket_form, 'review_form': review_form})

@login_required
def edit_review_view(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
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
            return redirect('feed')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'reviews/edit_ticket.html', {'form': form, 'ticket': ticket})

@login_required
def feed_view(request):
    followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    reviews = Review.objects.filter(user__in=followed_users) | Review.objects.filter(user=request.user)
    reviews = reviews.annotate(last_action_time=F('time_created')).order_by('-last_action_time')
    tickets = Ticket.objects.filter(Q(author__in=followed_users) | Q(author=request.user))
    tickets = tickets.annotate(last_action_time=F('created_at')).order_by('-last_action_time')
    return render(request, 'reviews/feed.html', {'reviews': reviews, 'tickets': tickets})

@login_required
def followers_view(request):
    followers = UserFollows.objects.filter(followed_user=request.user)
    return render(request, 'reviews/followers.html', {'followers': followers})

@login_required
def user_profile_view(request):
    user = request.user
    return render(request, 'reviews/user_profile.html', {'user': user})
