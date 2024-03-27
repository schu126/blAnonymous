import sqlite3
from hashlib import sha256

CONN = sqlite3.connect('database.db')
CURSOR = CONN.cursor()

class User:
    @classmethod
    def create_table(cls):
        """Create the user table if it doesn't already exist."""
        sql = """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the user table if it exists."""
        sql = "DROP TABLE IF EXISTS user;"
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def register(cls, name, password):
        """ register a new user with a username and password """
        try:
            hashed_password = sha256(password.encode()).hexdigest()  # Consider using bcrypt or Argon2 here
            sql = "INSERT INTO user (name, password) VALUES (?, ?);"
            CURSOR.execute(sql, (name, hashed_password))
            CONN.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error registering user: {e}")
            return False

    @classmethod
    def authenticate(cls, name, password):
        """ Check if account exists and password matches, then return authentication status and user_id """
        hashed_password = sha256(password.encode()).hexdigest()
        sql = "SELECT id FROM user WHERE name = ? AND password = ?;"
        CURSOR.execute(sql, (name, hashed_password))
        user = CURSOR.fetchone()
        if user:
            print("Welcome Back!")
            return True, user[0]  # Return True and user_id
        else:
            print("Authentication failed: Invalid username or password.")
            return False, None  # Return False and None for user_id

    @classmethod
    def update(cls, user_id, new_name=None, new_password=None):
        """Update the username and/or password of an existing user."""
        try:
            if new_name:
                sql = "UPDATE user SET name = ? WHERE id = ?;"
                CURSOR.execute(sql, (new_name, user_id))
            if new_password:
                hashed_password = sha256(new_password.encode()).hexdigest()  # Consider using bcrypt or Argon2 here
                sql = "UPDATE user SET password = ? WHERE id = ?;"
                CURSOR.execute(sql, (hashed_password, user_id))
            CONN.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error updating user: {e}")

    @classmethod
    def delete(cls, user_id):
        """Delete a user from the database."""
        sql = "DELETE FROM user WHERE id = ?;"
        CURSOR.execute(sql, (user_id,))
        CONN.commit()

