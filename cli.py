from __init__ import CURSOR, CONN
from User import User
from Posts import Posts
import datetime

session = {'user_id': None}

def initialize_app():
    User.create_table()
    Posts.create_table()

def main_menu():
    print("Welcome to blAnonymous Blog Center")
    print("1. Log In\n2. Register\n3. Exit")
    choice = input("Choose an option: ")
    if choice == "1":
        login()
    elif choice == "2":
        register()
    elif choice == "3":
        exit()
    else:
        print("Invalid choice. Please try again.")
        main_menu()

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    authenticated, user_id = User.authenticate(username, password)  # Assuming authenticate returns (bool, user_id)
    if authenticated:
        session['user_id'] = user_id  # Store user_id in session
        user_dashboard()
    else:
        print("Login failed. Please try again.")
        main_menu()

def register():
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    User.register(username, password)
    print("Registration successful. Please log in.")
    main_menu()

def user_dashboard():
    print("User Dashboard")
    print("1. View Posts\n2. Create Post\n3. Logout")
    choice = input("Choose an option: ")
    if choice == "1":
        view_posts()
    elif choice == "2":
        create_post()
    elif choice == "3":
        main_menu()
    else:
        print("Invalid choice. Please try again.")
        user_dashboard()

def view_posts():
    posts = Posts.get_all()
    if not posts:
        print("No posts available.")
    else:
        for post in posts:
            print(f"{post.id}: {post.title} - {post.publication_date}")
        post_id = input("Enter post ID to view details, or 'b' to go back: ")
        if post_id.lower() == 'b':
            user_dashboard()
        else:
            view_individual_post(int(post_id))

def view_individual_post(post_id):
    post = Posts.find_by_id(post_id)
    if post:
        print(f"Title: {post.title}\nContent: {post.content}\nDate: {post.publication_date}\nLikes: {post.likes}, Dislikes: {post.dislikes}")
        print("1. Like\n2. Dislike\n3. Go Back")
        action = input("Choose an option: ")
        if action == "1":
            Posts.like_post(post_id)
            print("Post liked.")
        elif action == "2":
            Posts.dislike_post(post_id)
            print("Post disliked.")
        elif action == "3":
            view_posts()
        else:
            print("Invalid choice.")
        
        print(f"Updated - Likes: {post.likes}, Dislikes: {post.dislikes}")
        view_individual_post(post_id)
        post = Posts.find_by_id(post_id)

    else: 
        print("Post not found.")
        view_posts()
       

    
def create_post():
    
    title = input("Enter post title: ")
    content = input("Enter post content: ")
    publication_date = input("Enter publication date (MM-DD-YYYY): ")

    # validate the publication date format
    try:
        datetime.datetime.strptime(publication_date, "%m-%d-%Y")
        # Use the session's user_id as author_id
        author_id = session['user_id']
        Posts.create(title, content, publication_date, author_id)
        print("Post created successfully.")
    except ValueError:
        print("Invalid date format. Please use MM-DD-YYYY.")
    
    user_dashboard()



if __name__ == "__main__":
    initialize_app()
    main_menu()
