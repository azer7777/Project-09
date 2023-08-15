# Project-09

# LitReview

LitReview is a web application that allows users to create, review, and interact with posts and reviews related to various topics. Users can follow each other, create posts, write reviews, and engage in discussions.

## Features

- User registration and authentication
- Create, edit, and delete posts
- Write and edit reviews for posts
- Follow other users and see their posts and reviews in the feed
- View posts and reviews from followed users and own posts and reviews in the feed
- Block and unblock followers
- Responsive and modern user interface

## Installation

1. Clone the repository:
````
git clone https://github.com/yourusername/LitReview.git
````
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
Explore the feed to see posts and reviews from users you follow.
Create new posts and write reviews for existing posts.
Edit and delete your posts and reviews.
Follow or block other users to manage your connections.
Visit the admin panel at http://127.0.0.1:8000/admin/ to manage users, posts, and reviews.
