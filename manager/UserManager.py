# QtFusion, AGPL-3.0 license
import os
from PIL import Image
import sqlite3
import hashlib


class UserManager:
    """A class for managing a database of users.

    This class provides methods for registering users, getting user data,
    changing a user's password, changing a user's avatar, and verifying a user's login credentials.

    Attributes:
        conn (sqlite3.Connection): Connection to the SQLite database.
        cursor (sqlite3.Cursor): Cursor for database operations.
    """

    def __init__(self, db_name):
        """Initialize the UserManager with a SQLite database.

        Args:
            db_name (str): Name of the SQLite database file.
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't already exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                avatar TEXT
            )
        ''')
        self.conn.commit()

    def hash_password(self, password):
        """Hash a password using SHA-256.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_avatar(self, avatar_path):
        """Check if an avatar file is valid.

        Args:
            avatar_path (str): Path to the avatar file.

        Returns:
            int: 0 if the avatar is valid, -1 if the file does not exist, -2 if the file is not a valid image.
        """
        if not os.path.isfile(avatar_path):
            return -1  # Avatar file does not exist
        try:
            Image.open(avatar_path)
        except IOError:
            return -2  # Invalid image file
        return 0

    def register(self, username, password, avatar):
        """Register a new user.

        Args:
            username (str): The username of the new user.
            password (str): The password of the new user.
            avatar (str): Path to the avatar file of the new user.

        Returns:
            int: 0 if the registration was successful, -1 if the username already exists,
            -2 if the password is too short, -3 if the avatar is not valid.
        """
        if self.get_user(username):
            return -1  # Username already exists
        if len(password) < 6:
            return -2  # Password must be at least 8 characters long
        avatar_status = self.verify_avatar(avatar)
        if avatar_status != 0:
            return -3
        hashed_password = self.hash_password(password)
        self.cursor.execute('''
                    INSERT INTO users (username, password, avatar)
                    VALUES (?, ?, ?)
                ''', (username, hashed_password, avatar))
        self.conn.commit()
        return 0

    def get_user(self, username):
        """Get data for a user.

        Args:
            username (str): The username of the user.

        Returns:
            tuple: The user's data, or None if the user does not exist.
        """
        self.cursor.execute('''
            SELECT * FROM users WHERE username = ?
        ''', (username,))
        return self.cursor.fetchone()

    def change_password(self, username, new_password):
        """Change a user's password.

        Args:
            username (str): The username of the user.
            new_password (str): The user's new password.

        Returns:
            int: 0 if the password was changed successfully, -1 if the user does not exist,
            -2 if the new password is too short.
        """
        if not self.get_user(username):
            return -1  # User does not exist
        if len(new_password) < 6:
            return -2  # Password must be at least 6 characters long
        hashed_password = self.hash_password(new_password)
        self.cursor.execute('''
            UPDATE users
            SET password = ?
            WHERE username = ?
        ''', (hashed_password, username))
        self.conn.commit()
        return 0

    def change_avatar(self, username, password, new_avatar):
        """Change a user's avatar.

        Args:
            username (str): The username of the user.
            password (str): The user's password.
            new_avatar (str): Path to the new avatar file.

        Returns:
            int: 0 if the avatar was changed successfully, -1 if the user does not exist,
            -2 if the password is incorrect, -3 if the avatar is not valid.
        """
        login_status = self.verify_login(username, password)
        if login_status != 0:
            return -2 if login_status == -2 else -1
        avatar_status = self.verify_avatar(new_avatar)
        if avatar_status != 0:
            return -3
        self.cursor.execute('''
            UPDATE users
            SET avatar = ?
            WHERE username = ?
        ''', (new_avatar, username))
        self.conn.commit()
        return 0

    def verify_login(self, username, password):
        """Verify a user's login credentials.

        Args:
            username (str): The username of the user.
            password (str): The user's password.

        Returns:
            int: 0 if the credentials are valid, -1 if the user does not exist, -2 if the password is incorrect.
        """
        user = self.get_user(username)
        if not user:
            return -1
        hashed_password = self.hash_password(password)
        if hashed_password != user[1]:
            return -2
        return 0

    def get_avatar(self, username):
        """Get the avatar of a user.

        Args:
            username (str): The username of the user.

        Returns:
            str: The path of the avatar, None if the user does not exist.
        """
        user = self.get_user(username)
        if not user:
            return -1
        return user[2]

    def delete_user(self, username, password):
        """Delete a user account.

        Args:
            username (str): The username of the user.
            password (str): The user's password.

        Returns:
            int: 0 if the account was deleted successfully, -1 if the user does not exist,
            -2 if the password is incorrect.
        """
        login_status = self.verify_login(username, password)
        if login_status != 0:
            return -2 if login_status == -2 else -1
        self.cursor.execute('''
            DELETE FROM users
            WHERE username = ?
        ''', (username,))
        self.conn.commit()
        return 0
