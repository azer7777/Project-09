# Project-09

# LitReview

LitReview is a web application that allows users to request reviews of books or articles, by creating a ticket,
read reviews of books or articles, publish reviews of books or articles. Users can follow each other.

## Features

- User registration and authentication
- Create, edit, and delete tickets
- Write and edit reviews for tickets
- Follow and unfollow other users and see their posts in the feed
- View posts from followed users and own posts and reviews in the Feed and Posts
- Block and unblock followers
- Responsive and modern user interface

## Installation

1. Clone the repository:
````
git clone https://github.com/azer7777/Project-09.git
cd LitReview
````
2. Create a virtual environment and activate it:
````
python3 -m venv venv 
source venv/bin/activate
````
3. Install dependencies:
````
pip install -r requirements.txt
````
4. Run migrations:
````
python manage.py migrate
````
5. Create a superuser to manage the admin panel:
````
python manage.py createsuperuser
````
6. Start the development server:
````
python manage.py runserver
````
7. Access the application at `http://localhost:8000/`

##Usage
Register a new account or log in.
Explore the feed to see tickets and reviews from users you follow.
Create new posts and write reviews for existing tickets.
Edit and delete your tickets and reviews.
Follow or block other users to manage your connections.
Visit the admin panel to manage users, tickets, and reviews.
