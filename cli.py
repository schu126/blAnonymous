from __init__ import CURSOR, CONN
from User import User
from Posts import Posts
import os
import datetime

session = {'user_id': None}

def initialize_app():
    User.create_table()
    Posts.create_table()

def main_menu():
    print("\nWelcome to blAnonymous")
    print("\n1. Log In\n2. Register\n3. Exit")
    choice = input("\nChoose an option: ")
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
        main_menu()

def register():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        username = input("Enter new username: ")
        password = input("Enter new password: ")
        success = User.register(username, password)
        if success:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Registration successful. Please log in.")
            main_menu()
        else:
            print("Username already exists, you're late to the game buddy. Be more original.")
            try_again = input("Try again? (y/n): ").lower()
            if try_again != 'y':
                os.system('cls' if os.name == 'nt' else 'clear')
                main_menu()

def user_dashboard():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("User Dashboard")
        print("\n1. View Posts\n2. Create Post\n3. Logout")
        choice = input("\nChoose an option: ")

        if choice == "1":
            view_posts()
        elif choice == "2":
            create_post()
        elif choice == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("You have successfully logged out.")
            main_menu()
        else:
            print("Invalid choice. Please try again.")
            user_dashboard()

def view_posts():
    os.system('cls' if os.name == 'nt' else 'clear')

    posts = Posts.get_all()
    if not posts:
        print("No posts available.")
    else:
        for post in posts:
            print(f"{post.id}: {post.title} - {post.publication_date}")
        post_id = input("\nEnter post ID to view details, or 'b' to go back: ")
        if post_id.lower() == 'b':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_dashboard()
        else:
            view_individual_post(int(post_id))

def view_individual_post(post_id):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
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
                # os.system('cls' if os.name == 'nt' else 'clear')
                view_posts()
            else:
                print("\nInvalid choice. Please select a valid option")
            
            # print(f"Updated - Likes: {post.likes}, Dislikes: {post.dislikes}")
            view_individual_post(post_id)
            post = Posts.find_by_id(post_id)

        else: 
            print("Post not found.")
            view_posts()
        

    
def create_post():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    title = input("Enter post title: ")
    content = input("Enter post content: ")
    publication_date = input("Enter publication date (MM-DD-YYYY): ")

    try:
        # Validate the publication date format and ensure title/content are not empty
        datetime.datetime.strptime(publication_date, "%m-%d-%Y")
        if title.strip() and content.strip(): 
            success = Posts.create(title, content, publication_date, session['user_id'])
            if success:
                print("Post created successfully. Now people can read your stuff.")
            else:
                print("Post creation failed. There might have been an issue saving to the database.")
        else:
            print("Title and content cannot be empty.")
    except ValueError:
        print("Invalid date format. Please use MM-DD-YYYY.")

    input("Press to see existing posts.")  # Give the user a chance to read the message before proceeding
    view_posts()  # Show the list of posts




if __name__ == "__main__":
    initialize_app()
    main_menu()
