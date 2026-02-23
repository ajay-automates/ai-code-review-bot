"""
User authentication module.
This code has several intentional bugs and security issues
to test the AI code review bot.
"""

import sqlite3
import hashlib

# BUG 1: Hardcoded database credentials
DB_PASSWORD = "admin123"
API_SECRET = "sk-secret-key-do-not-share-12345"

def get_user(username):
    """Fetch user from database."""
    # BUG 2: SQL Injection vulnerability
    conn = sqlite3.connect("users.db")
    query = f"SELECT * FROM users WHERE username = '{username}'"
    result = conn.execute(query)
    return result.fetchone()

def hash_password(password):
    """Hash a password for storage."""
    # BUG 3: Using MD5 (insecure, broken hash algorithm)
    return hashlib.md5(password.encode()).hexdigest()

def calculate_average_rating(ratings):
    """Calculate the average rating from a list."""
    # BUG 4: Division by zero if ratings is empty
    total = sum(ratings)
    return total / len(ratings)

def read_config(filepath):
    """Read configuration from a file."""
    # BUG 5: No error handling, no context manager
    f = open(filepath, 'r')
    data = f.read()
    config = eval(data)  # BUG 6: Using eval() on untrusted input
    return config

def process_items(items):
    """Process a list of items."""
    results = []
    # BUG 7: Modifying list while iterating
    for item in items:
        if item.get("status") == "invalid":
            items.remove(item)
        else:
            results.append(item["value"])
    return results

def login(username, password):
    """Authenticate a user."""
    user = get_user(username)
    if user:
        # BUG 8: Timing attack vulnerability (direct string comparison)
        if user[2] == hash_password(password):
            return {"status": "success", "token": API_SECRET}
        else:
            return {"status": "failed"}
    return {"status": "user not found"}
